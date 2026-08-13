---
tags: [quick-note, penpot, mcp, devops, nginx, homelab]
created: 2026-08-13
---

# Penpot MCP — Working Configuration Notes

> How the Penpot ↔ Hermes MCP connection was fixed and how to keep it alive.

## Architecture

```
┌──────────────┐   WebSocket   ┌───────────────┐   WS:4402   ┌──────────────┐
│  Penpot tab  │ ────────────► │  penpot-frontend│ ─────────► │  penpot-mcp  │
│  (browser)   │  /mcp/ws      │  (nginx 7009)  │             │  (4401 HTTP, │
└──────────────┘               └───────┬───────┘             │   4402 WS)   │
                                       │                     └──────┬───────┘
                                       │                            │
                              /mcp/stream (HTTP SSE)                │
                                       ▲                            │
┌──────────────┐   userToken URL      │                            │
│    Hermes    │ ─────────────────────┴────────────────────────────┘
│  (MCP client)│   https://design.panomete.com/mcp/stream?userToken=...
└──────────────┘
```

**Three links must ALL be alive:**
1. Browser → MCP server via WebSocket `/mcp/ws` (the "plugin instance")
2. Hermes → MCP server via HTTP stream `/mcp/stream`
3. Both authenticated with the **same userToken**

## The three bugs that broke it

### 1. nginx buffering killed the stream (host `design.conf`)
- `proxy_buffering on` (default) → SSE events stuck in 4KB buffer
- `proxy_read_timeout 60s` (default) → stream killed after 1 min
- `proxy_http_version 1.0` (default) → wrong semantics for long-lived streams

**Fix** — dedicated `/mcp/` location: `proxy_buffering off`, `proxy_read_timeout 1d`, `proxy_send_timeout 1d`, HTTP/1.1, `Connection ""`, `chunked_transfer_encoding on`, `gzip off`.

### 2. Same buffering problem inside the frontend container
`penpotapp/frontend:2.16` bakes `/mcp/stream` proxying into the image with buffering on + 300s timeout.

**Fix** — bind-mount a corrected config:
```yaml
# docker-compose.yaml (frontend service)
volumes:
  - penpot_assets:/opt/data/assets
  - ./nginx/mcp-locations.conf:/etc/nginx/overrides/server.d/mcp-locations.conf:ro
```

### 3. `Connection ""` broke the WebSocket handshake 🚨
The first fix matched `/mcp/` **including** `/mcp/ws`, stripping `Connection: upgrade` → browser bridge could never register ("No plugin instance connected").

**Fix** — dedicated `/mcp/ws` location **BEFORE** `/mcp/`:
```nginx
location /mcp/ws {
    proxy_pass http://127.0.0.1:7009;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    # + Host/Forwarded headers, proxy_read_timeout 1d
}
```

## The token gotcha

- The token in `design.conf` is **NOT** the same as the Hermes config token
- Regenerating the MCP key in Penpot (**Integrations → REGENERATE MCP KEY**) changes the token → must update Hermes config too
- Symptoms of stale token: MCP server logs show `userTokenFp=<different>` for browser vs Hermes calls

**How to verify token sync:** check `docker logs penpot-penpot-mcp-1` — both the browser WS registration and Hermes tool calls must show the **same `userTokenFp`**.

## Reconnect checklist (when it breaks)

| # | Check |
|---|-------|
| 1 | Penpot file tab open in browser (the file you want to edit) |
| 2 | Click **MCP → "Connect here"** in Penpot toolbar (no dialog in 2.16 — button flips to Connected) |
| 3 | Hermes config has matching URL: `C:\Users\Admin\AppData\Local\hermes\profiles\ui-ux\config.yaml` → `mcp_servers.penpot.url` |
| 4 | Restart Hermes after config change |
| 5 | Verify in logs: browser WS registered + Hermes session with same `userTokenFp` |

## Key locations

| What | Where |
|------|-------|
| Host nginx config | `/etc/nginx/sites-available/design.conf` (homelab) |
| Frontend override | `/home/flowero/application/penpot/nginx/mcp-locations.conf` (homelab) |
| Docker compose | `/home/flowero/application/penpot/docker-compose.yaml` |
| Penpot stack | `penpotapp/frontend:2.16`, `penpotapp/mcp:2.16`, `penpotapp/backend:2.16` |
| MCP server logs | `docker logs penpot-penpot-mcp-1` |
| Hermes config | `C:\Users\Admin\AppData\Local\hermes\profiles\ui-ux\config.yaml` |
| Penpot MCP settings | Penpot → Settings → Integrations (MCP Server, Beta) |
| SSH to homelab | `ssh -i ~/.ssh/id_homelab flowero@remote.panomete.com` |

## Diagnostic commands

```bash
# WS handshake through full chain (should be 101)
curl -s -o /dev/null -w 'HTTP %{http_code}\n' 'http://127.0.0.1/mcp/ws?userToken=test' \
  -H 'Host: design.panomete.com' -H 'Connection: Upgrade' -H 'Upgrade: websocket' \
  -H 'Sec-WebSocket-Version: 13' -H 'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ=='

# Watch MCP server activity
docker logs -f penpot-penpot-mcp-1

# Validate nginx after edits
sudo nginx -t && sudo systemctl reload nginx
```

> External `curl` WS test returns **426** — that's curl lacking WebSocket-over-HTTP/2, NOT a server problem. Browsers handle it natively. Test WS from inside the server instead.

## Gotcha: Penpot "Connect here" has no dialog (v2.16)

The MCP button → "Connect here" emits a `connect-mcp-plugin` event and opens the WS directly. There is **no dialog**. The button flipping to "Connected" IS the success signal. If the browser connects without token → check the MCP server logs for `WARN Connection attempt without userToken` → hard-refresh the file tab (Ctrl+F5) so the frontend picks up the key from profile state.
