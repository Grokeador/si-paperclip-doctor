# SI-Paperclip-Doctor

Open-source **Diagnostic Patcher, Deadlock Unlocker & `$0.00` Local Ollama/Claude Code Configurator** for **[Paperclip AI (`paperclipai/paperclip`)](https://github.com/paperclipai/paperclip)**.

While Paperclip AI makes it easy to orchestrate autonomous AI agent companies with org charts and heartbeats, self-hosters on Windows hit several documented runtime blockers (`#21785`, `#21777`, `#21759`, `#21789`, `#21753`) and risk unexpected cloud API bills. **SI-Paperclip-Doctor** solves all of them deterministically in Python with zero external dependencies, SHA-256 backups, and a Dark Desktop Control Center.

## What SI-Paperclip-Doctor Fixes

| Module | Paperclip AI Upstream Issue | SI-Paperclip-Doctor Fix |
| --- | --- | --- |
| **1. Deadlock & Fold Recovery Unlocker** | Issues **#21785** & **#21777**: Interrupted legacy Pi runs leave permanent accounting locks & re-create conversation fold recovery holds every 30s | Safely clears `accounting_lock`, `recovery_hold`, and stale `.lock`/`.hold` files inside SQLite & JSON without deleting workspace history |
| **2. Governance Schema Sanitizer** | Issue **#21759**: Saving Company settings fails with `Unrecognized key: connection_intent` | Recursively removes invalid `connection_intent` keys from `interaction_governance` configs before save |
| **3. Doc Key & O(V+E) Blocker Graph Fix** | Issues **#21789** & **#21753**: Document key `list` crashes Task Viewer; shared diamond blockers cause exponential slowdowns | Sanitizes reserved `list` keys (`doc_list`) and runs linear `O(V+E)` Kahn topological deduplication & cycle breaking |
| **4. `$0.00` Local Ollama + Claude Code Cap** | Risk of runaway GPT-4o / Anthropic API spend across autonomous agent heartbeats | Generates `paperclip_local_harness.json` + `.paperclip.local.env` wired to local `127.0.0.1:11434/v1` + Claude Code at `$0.00/mo` |

## Quick Start

```bash
# Audit an existing Paperclip AI workspace
python si_paperclip_doctor.py scan --workspace "C:\Path\To\PaperclipWorkspace"

# Patch bugs + configure $0.00 local Ollama & Claude Code (creates SHA-256 backup first)
python si_paperclip_doctor.py repair --workspace "C:\Path\To\PaperclipWorkspace"

# Launch Dark Desktop Web Control Center
python si_paperclip_doctor.py web --workspace "C:\Path\To\PaperclipWorkspace" --port 8791

# Rollback to untouched original files anytime
python si_paperclip_doctor.py rollback --workspace "C:\Path\To\PaperclipWorkspace"
```

## Automated Tests

```bash
python -m unittest test_doctor.py -v
```
