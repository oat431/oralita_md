---
name: mcp-server-patterns
description: "Add or troubleshoot MCP servers in Hermes Agent."
version: 1.0.0
author: OraMesLita
license: MIT
metadata:
  hermes:
    triggers:
      - "add mcp server"
      - "mcp configuration"
      - "filesystem mcp"
      - "mcp not working"
      - "mcp tools missing"
      - "add searxng"
      - "add brave search"
      - "mcp server setup"
    related_skills: [hermes-agent]
---

# MCP Server Configuration Patterns

Practical patterns for configuring MCP servers in Hermes Agent. Covers common setups, pitfalls, and optimization techniques.

## Quick Reference

### Filesystem MCP — Parent Directory Access

**Key insight:** Specifying a parent directory grants access to ALL subdirectories automatically. No wildcards needed.

```yaml
# ❌ Verbose — listing every subdirectory
filesystem:
  command: npx
  args:
    - -y
    - '@modelcontextprotocol/server-filesystem'
    - F:\projects\app1
    - F:\projects\app2
    - F:\projects\app3

# ✅ Clean — parent directory covers all subdirs
filesystem:
  command: npx
  args:
    - -y
    - '@modelcontextprotocol/server-filesystem'
    - F:\projects          # ALL subdirs automatically accessible
    - F:\obsidian_note     # ALL Obsidian vaults
```

**Why this works:** The server treats specified directories as allowed roots. Any path under them is automatically accessible, including future subdirectories.

### MCP SDK Installation

**Prerequisite:** The `mcp` Python package must be installed for MCP support.

```bash
# Install MCP SDK
pip install mcp

# Verify installation
python -c "import mcp; print('MCP SDK installed')"
```

**Pitfall:** If you see "MCP SDK not available -- skipping MCP tool discovery", the package is missing. MCP support is silently disabled without it.

### MCP Roots Protocol

For dynamic directory updates without server restart, use MCP Roots:

```yaml
filesystem:
  command: npx
  args:
    - -y
    - '@modelcontextprotocol/server-filesystem'
    # No directories specified — client provides via Roots protocol
```

**When to use:** When you need runtime directory updates via `roots/list_changed` notifications. Most users should stick with explicit directory args.

## Common MCP Server Configurations

### SearXNG — Privacy-respecting Web Search

```yaml
searxng:
  command: npx
  args:
    - -y
    - mcp-searxng
  env:
    SEARXNG_URL: "http://your-searxng-instance:8080"
  timeout: 30
```

**Why:** Replaces `ddgs` (often broken), private, no API key needed.

### Brave Search — High-quality Web Search

```yaml
brave-search:
  command: npx
  args:
    - -y
    - "@brave/brave-search-mcp-server"
  env:
    BRAVE_API_KEY: "your-brave-api-key"  # Free at brave.com/search/api
  timeout: 30
```

### Obsidian MCP — Direct Vault Manipulation

```yaml
obsidian:
  command: npx
  args:
    - -y
    - "@fazer-ai/mcp-obsidian"
  env:
    OBSIDIAN_API_KEY: "your-obsidian-api-key"  # Enable in Obsidian settings
    OBSIDIAN_HOST: "localhost"
    OBSIDIAN_PORT: "27123"
  timeout: 30
```

### PostgreSQL — Database Access

```yaml
postgres:
  command: npx
  args:
    - -y
    - '@modelcontextprotocol/server-postgres'
    - postgresql://user:pass@localhost:5432/dbname
```

### GitHub — Repository Management

```yaml
github:
  command: npx
  args:
    - -y
    - '@modelcontextprotocol/server-github'
  env:
    GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxxxxxxxxx"
```

## Transport Types

### Stdio Transport (command-based)

```yaml
server_name:
  command: "npx"             # Executable to run
  args: ["-y", "pkg-name"]   # Command arguments
  env:                       # Environment variables for subprocess
    SOME_API_KEY: "value"
  timeout: 120               # Per-tool-call timeout (seconds)
  connect_timeout: 60        # Initial connection timeout (seconds)
```

### HTTP Transport (url-based)

```yaml
server_name:
  url: "https://mcp.example.com/mcp"
  headers:
    Authorization: "Bearer sk-..."
  timeout: 180
  connect_timeout: 60
```

**Note:** A server config must have either `command` (stdio) or `url` (HTTP), not both.

## Security Considerations

### Environment Variable Filtering

For stdio servers, Hermes only passes safe baseline variables:
- `PATH`, `HOME`, `USER`, `LANG`, `LC_ALL`, `TERM`, `SHELL`, `TMPDIR`
- Any `XDG_*` variables

All other environment variables are excluded unless explicitly added via `env`. This prevents accidental credential leakage.

```yaml
github:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-github"]
  env:
    # Only this token is passed to the subprocess
    GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_..."
```

### Credential Stripping in Error Messages

Failed MCP tool calls automatically redact credential patterns:
- GitHub PATs (`ghp_...`)
- OpenAI-style keys (`sk-...`)
- Bearer tokens
- Generic `token=`, `key=`, `API_KEY=`, `password=`, `secret=` patterns

## Troubleshooting

### "MCP SDK not available -- skipping MCP tool discovery"

```bash
pip install mcp
```

### "No MCP servers configured"

Check `~/.hermes/config.yaml` has `mcp_servers` key with at least one entry.

### "Failed to connect to MCP server 'X'"

Common causes:
- **Command not found:** Ensure `npx`, `uvx`, or the command is on PATH
- **Package not found:** For npx servers, add `-y` to auto-install
- **Timeout:** Increase `connect_timeout`
- **Port conflict:** For HTTP servers, verify URL is reachable

### Tools not appearing

- Check server is under `mcp_servers` (not `mcp` or `servers`)
- Verify YAML indentation
- Tool names are prefixed: `mcp_{server}_{tool}`
- Look at startup logs for connection messages

### Connection keeps dropping

Client retries up to 5 times with exponential backoff (1s, 2s, 4s, 8s, 16s, capped at 60s). If fundamentally unreachable, gives up after 5 attempts.

## Pitfalls

- **Don't list every subdirectory.** Specify parent directories instead — the server grants access to all subdirs automatically.
- **Don't forget `-y` for npx servers.** Without it, npx may prompt for installation, which hangs in automated environments.
- **Don't put secrets in `args`.** Use `env` for API keys and tokens. Args are visible in process listings.
- **Don't use both `command` and `url`.** A server config must have one or the other, not both.
- **Don't assume MCP tools are available.** Check `hermes mcp list` to verify server status and tool discovery.
- **Don't skip the MCP SDK.** Without `pip install mcp`, MCP support is silently disabled.

## Verification

After adding MCP servers:

```bash
# Check server status
hermes mcp list

# Verify tools are discovered
hermes tools | grep mcp_

# Test a specific tool
hermes chat -q "List files in F:\projects using the filesystem MCP"
```

## Notes

- MCP tools are called synchronously from the agent's perspective but run asynchronously on a dedicated background event loop
- Server connections are persistent and shared across all conversations in the same agent process
- Adding or removing servers requires restarting the agent (no hot-reload currently)
- The native MCP client is independent of `mcporter` — you can use both simultaneously