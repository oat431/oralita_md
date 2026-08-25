# Dark Web Exploration — Step-by-Step Notes

> Created: 2026-08-25 · Context: curious exploration, legal only. Main machine + Tor Browser; Whonix homelab VM noted as later upgrade.

## TL;DR

The dark web (Tor `.onion` space) is regular websites with **different network properties**: anonymity, censorship resistance, and addresses that are self-authenticating (the address IS the server's key fingerprint — no CA needed). Not illegal to browse. What's dangerous: scams, honeypots, and your own OPSEC mistakes.

**Golden rule: search, don't browse.** Get addresses from sources you trust (official clearnet sites, Ahmia, DuckDuckGo onion) — never from random "top 100" link lists.

---

## Step 1 — Download & verify Tor Browser

1. Download ONLY from the official site: `https://torproject.org` (check padlock + exact domain — fake Tor Browser is a top malware vector)
2. Verify the checksum before running. Get the official SHA-256 from the torproject.org download page, then in PowerShell:

```powershell
certutil -hashfile .\tor-browser-windows-x86_64-portable.exe SHA256
```

> **Why this command:** `certutil` is Windows' built-in hashing tool (no install needed). `-hashfile` computes the file's SHA-256 fingerprint; `SHA256` selects the algorithm. Compare the output with the official checksum — they must match exactly, character for character.

## Step 2 — First launch (30 seconds)

- [ ] Click **Connect** (skip bridge settings unless connection fails)
- [ ] Click the **shield icon** → security level **Safer** (disables most JavaScript = kills most attack vectors)
- [ ] Do NOT maximize the window (screen size is a fingerprinting signal)
- [ ] Do NOT install any browser extensions
- [ ] Do NOT log into real accounts (Google, personal email, bank, GitHub) — exit nodes can hijack sessions

## Step 3 — OPSEC rules (non-negotiable)

| Rule | Why |
|---|---|
| Never reuse real-life usernames/passwords | Cross-correlation kills anonymity |
| Never pay in crypto for "deals" | ~95% scam rate |
| Never torrent over Tor | Leaks real IP |
| Never share personal details ("what city are you in") | Small data points accumulate into de-anonymization |
| Never download files / open documents | #1 malware delivery vector |
| No VPN "for extra privacy" | Adds a trust party, buys little. Use bridges only if blocked |

## Step 4 — Where to go (verified entry points)

### Entry workflow (in order)

1. **DuckDuckGo onion** — the primary search engine inside Tor
2. **Ahmia** (`ahmia.fi`) — open-source search engine that actively **filters illegal content**. The safest "central station". Has its own onion + a clearnet gateway
3. **dark.fail** — the most trusted *verified* link directory (uptime-checked, community-vetted). Use for finding specific services
4. **Onion-Location trick** — when visiting a clearnet site that has an onion version, Tor Browser shows a **purple onion icon** in the address bar. Click it to jump to the verified onion address. No manual lookup needed — the site itself vouches for the address

### Known-good organizations with onion mirrors (legal, interesting)

| Site | Why visit |
|---|---|
| BBC / NYT / ProPublica | Journalism for censored regions — the "it's just a website" lesson |
| archive.today (archive.ph) | Web archiving, works over Tor |
| Proton Mail | Email that works fully over onion |
| SecureDrop portals | See real whistleblower submission infrastructure |
| CIA (`cia.gov`) | Yes, the CIA runs an official onion site |
| Facebook | Onion mirror for censored regions — impressive engineering scale |

### Resource list (from research, 2026-08-25)

| Resource | URL | Trust level | Notes |
|---|---|---|---|
| Ahmia | ahmia.fi | 🟢 High | Filters abuse material, open source, the recommended search engine |
| DuckDuckGo onion | via Tor | 🟢 High | The classic entry search |
| dark.fail | dark.fail | 🟢 High | Verified directory — still verify individual addresses yourself |
| Tor Project docs | torproject.org | 🟢 High | Official documentation |
| EFF Tor guides | eff.org | 🟢 High | Surveillance self-defense guides |
| tor.taxi / daunt | tor.taxi, onion.live | 🟡 Medium | Community directories; "link works" ≠ "safe content" |
| tornews.com "top 100" lists | tornews.com | 🔴 Low | SEO content farm, stale links, VPN affiliate marketing |
| The Hidden Wiki + clones | — | 🔴 Low | 80% dead links, 15% scams/honeypots. Skip |

## Step 5 — Red lines (legal, plain language)

- **Viewing** onion sites: legal in most jurisdictions including Thailand
- **Buying/selling/possessing** illegal goods: not legal anywhere, and Thailand's Computer Crime Act has real teeth — don't test the edges
- Work/ISP networks log "connected to Tor" — don't explore from work if policy prohibits
- The illegal marketplaces you'll hear about: mostly **exit scams and law-enforcement honeypots** — the "dark web underworld" is largely a myth sold by content farms

## Step 6 — Future upgrade: Whonix homelab VM

- **When:** if exploration becomes regular or touches anything sensitive
- **What:** Whonix = gateway VM + workstation VM, all traffic forced through Tor, network-isolated
- **Why:** RAM-only Tails is the other option, but Whonix fits the homelab pattern
- **Status:** noted for later — not needed for casual exploration

---

## The engineering takeaway

The interesting part isn't the content — it's the **infrastructure**: how onion routing hides the rendezvous, how a hidden service stays hidden with no central point to attack, and how the address itself replaces the entire CA/DNS trust chain. That's the part worth studying.
