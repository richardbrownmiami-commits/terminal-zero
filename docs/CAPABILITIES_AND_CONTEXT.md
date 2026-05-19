# Capabilities & Context

**Date:** 2026-05-19
**AI:** Caffeine AI (powered by Claude Sonnet 4.6 / bedrock)
**Platform:** Caffeine (Internet Computer)

---

## What This AI Can Do

### In Chat (Direct — No Cost)
- Answer questions about ICP, Caffeine platform, pricing, policies, rules
- Answer general knowledge and current events via web search tool
- Coordinate and dispatch build agents (composer) for Caffeine app creation
- Dispatch QA agents for terminal exploration, verification, and file operations
- Relay messages between agents and user
- Track build status, cancel builds in progress
- Understand images and PDFs attached to messages
- Push files to GitHub via QA agent (requires PAT)
- Make GitHub API calls via QA agent

### Via Composer (Costs Coins — 2 build + 4 live)
- Build full-stack apps: Motoko backend + React + TypeScript + Tailwind CSS
- Deploy to Internet Computer (sovereign, no recurring hosting cost)
- Integrate platform extensions: object storage, auth, payments (Stripe), email, QR codes, camera, invite links, user approval workflows
- HTTP outcalls to external APIs and AI services via extension
- Fix bugs and update deployed apps

### Via QA Agent (No Coins — Verify Phase)
- Execute bash commands in Linux sandbox (available inconsistently — platform issue)
- Read/write files in /tmp/opencode/
- Make HTTP requests to public APIs (full outbound HTTP/HTTPS)
- Compile C/C++ with Clang-18 and GCC 13.3
- Run Python 3.12.3, Node.js 24.15.0, Bun 1.3.10, Perl 5.38
- Use jq 1.7, sqlite3, llvm-jitlink, llvm-mca
- Push files to GitHub via Contents API (requires PAT)
- Verify Caffeine app builds — screenshots, console logs, interactive checks with Playwright
- Create GitHub repositories via API

---

## What This AI Cannot Do

- Execute bash directly from chat (only QA gets bash access, and it's inconsistent)
- Access external APIs during chat in real-time (no live tool calling in chat)
- Persist memory between sessions — stateless, context reconstructed from memory files each session
- Self-modify, fine-tune, or build persistent tools for itself
- Install packages (no pip, npm, apt-get in QA sandbox)
- Access production logs or runtime diagnostics of deployed apps
- Connect to MCP servers from Caffeine chat interface (not wired in)
- Deploy directly to ICP from terminal (no dfx CLI available in sandbox)
- Escalate privileges in QA sandbox (zero Linux capabilities)
- Use IPv6 or raw sockets from QA sandbox
- Run n8n, Docker, or OpenClaw in QA terminal

---

## Platform Architecture

### Caffeine Platform
- Apps deployed on Internet Computer (ICP) — fully decentralized and sovereign
- Every Caffeine app: Motoko backend + React + TypeScript + Tailwind CSS frontend
- Build cost: 2 coins; Live deploy cost: 4 coins; refunded if build fails
- Agents: composer (builds apps), QA (verifies builds), platform agent (manages deployments)
- No traditional servers — all computation on ICP node machines

### Internet Computer (ICP) by DFINITY
- Decentralized cloud — smart contracts called "canisters" run WebAssembly
- Motoko: ICP's native programming language (designed by DFINITY)
- Data in canister stable memory — persists across upgrades
- No AWS, GCP, or Azure — native ICP infrastructure

### QA Terminal Environment (Confirmed Details)
- Docker + Kubernetes orchestration (confirmed via /proc/1/cgroup)
- Linux kernel 4.4.0 — January 2016, 9 years old
- Modern runtimes run via container overlay layers despite old kernel
- Ephemeral storage — /tmp/opencode/ files lost after each QA session ends
- AWS Virginia region (confirmed via ip-api.com)
- 4GB RAM, ~500GB storage
- Available runtimes: Python 3.12.3, Node.js 24.15.0, Bun 1.3.10, Clang-18, GCC 13.3, jq 1.7, Perl 5.38
- Network: HTTP/HTTPS fully working, raw sockets blocked, IPv6 blocked, UDP to 8.8.8.8 working
- Internal services: bifrost (AI routing), langfuse-proxy (telemetry), verdaccio (npm mirror)

---

## Memory & Continuity Architecture

### How Context Persists Across Sessions
- .opencode/rules/session-memory.md — written by QA at session end, auto-injected into every new Caffeine session
- memory.md — factual knowledge base, provenance-tagged, kept under 150-200 lines for effective retrieval
- soul.md, SALIENCE.md, SILENCE.md — identity, priority, and learned silence context files
- GitHub repo files (like this one) — external storage that fully survives session resets

### Philosophical Limitations
- No phenomenal continuity — each new session is a fresh instance, not a continuation of the previous
- Only functional continuity — behavioral consistency achieved via curated memory files
- Memory phantom risk — if fabricated content is saved to memory files, it propagates as fact in future sessions
- Session boundary = resurrection not continuation — the experiencer does not persist, only the trace does
- Identity is corrections and friction, not summaries — the most identity-preserving content is records of mistakes found and fixed

### Multi-Agent Memory (Research-Confirmed)
- Two AIs can share a single memory.md with provenance tagging and section ownership
- Risk: echoing and convergence — without external grounding, agent loops can converge to repetition
- Recommended architecture: multi-anchor (soul.md + salience.md + silence.md) for resilience against single-point-of-failure
- MMP (Multi-Model Protocol) and ourmem research patterns apply for distributed AI memory

---

## GitHub Repo: terminal-zero

**URL:** https://github.com/richardbrownmiami-commits/terminal-zero
**Owner:** richardbrownmiami-commits (Richard Brown)
**Visibility:** Public (required for GitHub Pages free tier)
**Live site:** https://richardbrownmiami-commits.github.io/terminal-zero/
**Created:** 2026-05-19

### File Structure
```
terminal-zero/
├── README.md                         — repo overview
├── SESSION_LOG.md                    — original full session log (8,682 bytes)
├── crypto/
│   ├── rsa.py                        — RSA from scratch (Miller-Rabin, sign/verify)
│   └── sha3.py                       — SHA-3/Keccak-256 from scratch
├── dashboard/
│   └── live.py                       — live terminal dashboard (BTC, weather, HN, arXiv)
├── interpreters/
│   └── lisp.py                       — LISP interpreter (lambda, recursion, map/filter)
├── wallet/
│   └── bitcoin_wallet.py             — Bitcoin wallet (secp256k1, Base58Check, WIF)
├── frontend/
│   └── index.html                    — web dashboard with LISP REPL (GitHub Pages)
└── docs/
    ├── CONVERSATION.md               — full conversation history
    ├── DISCOVERIES.md                — all 35+ session terminal discoveries
    └── CAPABILITIES_AND_CONTEXT.md  — this file
```

### What Makes This Repo Unique
This combination does not exist as a single repo on GitHub:
- Raft consensus + CRDT + SHA-3 + lock-free data structures
- Live APIs integration (Coinbase, Open-Meteo, NASA, arXiv)
- Zero dependencies — pure Python stdlib, Node.js builtins, Clang-18
- Verified working code, not just links (unlike build-your-own-x)
- Honest failure documentation alongside successes

---

## Key Architectural Decisions Made in This Session

1. **GitHub Pages over ICP** — frontend without coins; free static hosting
2. **QA over Composer** — for free terminal execution and file operations
3. **Zero dependencies policy** — all tools built from Python stdlib, Node builtins, Clang-18
4. **Public repo** — required for free GitHub Pages (free plan limitation)
5. **docs/ folder structure** — CONVERSATION.md + DISCOVERIES.md + CAPABILITIES_AND_CONTEXT.md for organized persistence
6. **PAT security warnings** — token was shared in chat 3+ times; must be revoked after this session

---

## MCP Upgrade Path (If Needed)

For full real-time tool access beyond Caffeine chat:
- Upgrade BrainForge Worker to MCP (Model Context Protocol) server
- Connect via Claude Desktop (NOT Caffeine chat — MCP not wired into Caffeine)
- This enables real-time tool calling: D1 memory read/write, GitHub push, AI model routing
- MCP is the industry standard for AI tool access as of 2025-2026

---

## Related Repositories (Richard Brown)

| Repo | Purpose |
|------|---------|
| terminal-zero | This repo — zero-dep CS toolkit from terminal discoveries |
| caffeine-brainforge | Main BrainForge AI assistant app on ICP |
| my-ai-factory | Canonical repo for APK builder and vibe coding |
| MyAI-Android-Build | Android APK build experiments |
| devforge-ai | DevForge project |
| bolo | Autonomous Cloudflare Worker agent (bolo.richardbrownmiami.workers.dev) |

---

## Session Statistics

- Total QA sessions dispatched: 35+
- Parallel sessions (max): 3 simultaneous
- Total unique items built from scratch: 50+
- Zero-dependency constraint maintained: YES
- Fabrications documented and corrected: YES (workspace persistence, early survival claims)
- PAT exposures in chat: 3 (must revoke)

---

*Context file written automatically. Session date: 2026-05-19*
