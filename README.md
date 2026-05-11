# AI Agent Memory Template

> A structured, hierarchical memory system for AI agents, inspired by [memU](https://github.com/NevaMind-AI/MemU) (Memory as File System) and [Claude Code](https://code.claude.com/docs/zh-CN/memory) (Auto-memory + Trigger-based knowledge retrieval).

## Why this exists

AI agents forget everything between sessions. This template gives them a **file-based memory system** that survives restarts:

- **Knowledge** — domain expertise organized by topic, read on demand. Each entry has a **decay status** (`✅ 有效` / `⏳ 待验证` / `❌ 已过时`) for long-term maintainability.
- **Decisions** — irreversible choices with full **reasoning memory**: what was chosen, why, what alternatives were considered and rejected, and the constraints that drove the decision.
- **Context** — what's pending, what's blocked, what's currently known.
- **Auto-learning** — a rolling 200-line cache of recently learned lessons, using a **structured format** (`日期 | 类型 | 问题 | 根因 | 解法 | 状态`) for quick scanning.
- **Sleep-time compute** — memory writes happen **after** responding to the user, not during. Corrections and learnings are batched and processed without blocking the conversation.
- **Emotional memory** — relationship, rapport, user preferences (optional).

## Structure

```
memory/
├── claude-like/           -- Auto-learning (inspired by Claude Code)
│   ├── recent.md          -- Rolling 200-line cache of corrections and lessons
│   └── triggers.md        -- Keyword to knowledge file mapping
│
├── knowledge/             -- Domain expertise, read on demand
│   ├── INDEX.md           -- Cross-reference index
│   ├── git.md
│   ├── wsl.md
│   ├── proxy.md
│   ├── your-topic.md      -- Add as needed
│   └── ...
│
├── decisions/             -- Irreversible decisions with rationale
│   └── YYYY-MM-DD-topic.md
│
├── context/               -- Current state
│   ├── pending.md         -- Todo list
│   └── limitations.md     -- Known hard constraints
│
├── bonds/                 -- Emotional memory (relationship, rapport)
│   ├── profile.md         -- User personality and working style
│   ├── story.md           -- Shared history, milestones
│   └── vibe.md            -- Rapport, signals, unwritten rules
│
├── preferences/           -- User preferences
│   └── user.md
│
└── daily/                 -- Raw daily logs
    └── YYYY-MM-DD.md
```

## Real-world impact

> Measured across ~10 hours of practical use with a single AI agent.

### Before: no memory system

Every session starts blank. Previously solved problems are re-solved from scratch.

| Task | Attempts | Outcome |
|------|----------|---------|
| `git clone` behind SOCKS5 proxy | 5 | TLS handshake -> tried SSH -> searched docs -> 15 min |
| `wsl bash -c` with sudo | 2 | stuck on password prompt -> opened new terminal -> 3 min |
| `gh CLI` usage | 3 | `command not found` -> searched PATH -> 5 min |
| `pip install` in Ubuntu 26.04 | 2 | `externally-managed` -> searched -> 5 min |

### After: with memory system

Each solution is recorded once in `knowledge/`. The agent reads it before attempting.

| Task | Attempts | Outcome |
|------|----------|---------|
| `git clone` behind SOCKS5 proxy | 1 | `GIT_SSL_BACKEND=openssl` from `knowledge/git.md` -- 5 sec |
| `wsl bash -c` with sudo | 1 | `echo "password" | sudo -S` from `knowledge/wsl.md` -- 2 sec |
| `gh CLI` usage | 1 | full path from `knowledge/github.md` -- 3 sec |
| `pip install` in Ubuntu 26.04 | 1 | venv setup from `knowledge/wsl.md` -- 10 sec |

**Time saved per task: 3-15 minutes.** The ~3k token cost of loading `recent.md` at session start is recovered by avoiding a single mistake.

### Maintenance cost

- **Memory updates**: 5-10 seconds per correction (append to `recent.md`)
- **Consolidation**: 5 minutes when `recent.md` hits 200 rows (every few weeks)
- **Knowledge lookup**: 2-10 seconds per `read` call (only when trigger word matches)

## How it works

### For AI agents

Place a `MEMORY.md` file at your agent's workspace root with a navigation section pointing to the memory directory. The agent reads it at session start:

```
## Memory Navigation
- Lessons learned -> memory/claude-like/recent.md (auto-load)
- Domain knowledge -> memory/knowledge/ (trigger-based lookup)
- Pending tasks -> memory/context/pending.md
- Known limits -> memory/context/limitations.md
```

### Auto-learning workflow

1. **Agent is corrected** -> immediately appends to `claude-like/recent.md`
2. **Agent starts a session** -> reads `recent.md` first (capped at 200 lines)
3. **Over 200 lines** -> oldest entries are distilled into `knowledge/` and removed
4. **Keyword triggers** -> when conversation mentions "git", agent auto-reads `knowledge/git.md`

### Memory update enforcement

Memory updates are **NOT optional**. Configure your agent with these hard rules:

**End-of-session check (mandatory):**
At the end of every conversation, the agent must check:
- `claude-like/recent.md` — pitfalls, decisions, knowledge from this session
- `knowledge/` — new tools, config changes
- `daily/YYYY-MM-DD.md` — what happened today
- `context/pending.md` — unfinished items
- `triggers.md` — new trigger keywords

**Start-of-session check (complementary):**
At the start of every new session, check if the previous session left any memory updates pending. If so, fill them in immediately.

**Pitfall/immediate logging:**
When hitting a pitfall or making a decision during conversation, log it IMMEDIATELY. Do not wait for session end.

> **Status after 10+ hours of practical use:** Without enforcement, the agent logged daily summaries but failed to update `knowledge/` and `claude-like/recent.md` consistently. After adding forced update rules (same priority as security redlines), all memory components were maintained reliably across sessions.

## Applicability

This template works with any AI agent that reads files and writes to a workspace directory. The method of "loading" varies by platform:

### By Agent

| Agent | How to use |
|-------|-----------|
| **OpenClaw** | Set `agents.defaults.workspace` in openclaw.json to point at the parent of `memory/`. Place `MEMORY.md` at workspace root. Convert `knowledge/` files into Skill format for auto-triggered retrieval. |
| **Claude Code** | Place `CLAUDE.md` at project root with `@MEMORY.md` import. Or symlink: `ln -s memory/../MEMORY.md ./CLAUDE.md`. |
| **Cline** | Set `memory/` path in Cline's custom instructions. Reference file paths in your rules. |
| **Cursor / Windsurf** | Add key knowledge points from `knowledge/` to `.cursorrules` or project rules. |
| **Codex CLI** | Include `MEMORY.md` content in your task prompt at session start. |
| **Any CLI agent** | Pipe the template structure into the initial prompt: `cat MEMORY.md knowledge/git.md` |

### By Operating System

| OS | Considerations |
|----|--------------|
| **Windows** | Use `A:` or `C:` paths. Git needs `GIT_SSL_BACKEND=openssl` behind SOCKS5 proxies. `wsl bash -c` wraps Linux tools. |
| **macOS** | Native Unix paths. Symlinks work out of the box. |
| **Linux** | Native path support. Best compatibility with tmux-based swarms. |
| **WSL2** | Files on `/mnt/` are accessible from both Windows and Linux. Use Mirrored networking for proxy sync. |

### Customization Tips

- **Minimal setup**: Just use `claude-like/recent.md` plus one `knowledge/` file for your most common topic.
- **Team setup**: Share `knowledge/` and `decisions/` via git. Keep `bonds/` and `preferences/` local.
- **Swarm setup** (ClawTeam, agent teams): The leader agent uses `MEMORY.md`. Workers are stateless.

> See [ROADMAP.md](ROADMAP.md) for known limitations and planned improvements.

## How it compares to existing solutions

| Feature | This template | Awareness-Local (217 stars) | cortex (239 stars) | clawbrain (25 stars) |
|---------|:---:|:---:|:---:|:---:|
| Zero dependencies (copy and use) | Yes | No (needs MCP server) | No (needs Python service) | No (needs plugin) |
| Multi-agent support | 8 agents table | MCP only | framework-specific | OpenClaw only |
| Reasoning memory (alternatives) | Yes (decisions/ format) | No | No | No |
| Emotional memory (soul/bonding) | Yes (bonds/) | No | No | Yes (Soul + Bonding) |
| Memory decay (status markers) | Yes (rolling) | No | No | No |
| Auto-learning (rolling cache) | Yes (recent.md) | via MCP | No | No |
| Trigger-based retrieval | Yes (triggers.md) | semantic search | Yes | No |
| Sleep-time compute | Yes (structured rule) | No | No | No |
| Structured summary format | Yes (type/cause/solution/status) | No | No | No |
| Local-first, no cloud | Yes | Yes | optional | Yes |

**Why build on templates instead of services?** No lock-in, no runtime, transparent, versionable.

> Services like cortex and Awareness-Local are better if you need semantic search across thousands of entries. Templates are better if you want simplicity, transparency, and zero operational overhead.

## When to use this template vs a memory service

| Scenario | Template (this repo) | Memory service (cortex, Awareness-Local) |
|---------|:---:|:---:|
| Single user, personal agent | Best fit | Overkill |
| Team of 10+ users sharing memory | Not designed for this | Best fit |
| Fewer than 500 memory entries | Lightweight | Fine but extra ops |
| 5000+ entries with semantic search | No vector search | Purpose-built |
| Zero ops, no deploy | Copy and go | Needs server/database |
| Need to git-track memory changes | Built on files | Binary or DB |
| Want AI to auto-extract memories | Manual logging | Automatic |
| Need cross-reference reasoning | File-by-file only | Graph queries |
| Building a demo / prototype | Fast setup | Too heavy |
| Building for production scale | Single-agent limit | Multi-tenant |

**Key insight:** Personal use, under 500 entries, single agent -> template. Team, thousands of entries, need auto-discovery -> service. Want to start simple and upgrade later? Start here. All memory is markdown files -- portable to any system when you outgrow this approach.

## Inspired by

| Source | What we borrowed |
|--------|-----------------|
| [memU](https://github.com/NevaMind-AI/memU) | Memory as hierarchical file system (categories/facts like folders/files) |
| [Claude Code Memory](https://code.claude.com/docs/zh-CN/memory) | Auto-learning cache, bounded context (200 lines), separate knowledge vs memory |
| [Claude Code Best Practices](https://code.claude.com/docs/zh-CN/best-practices) | Trigger-based retrieval, "correct -> log -> apply" loop |

## Version History

| Version | Date | Notes |
|---------|------|-------|
| v2.0.3 | 2026-05-12 | Fix: forced memory update rules + start/end-of-session checks + immediate logging + template file |
| v2.0.2 | 2026-05-10 | Fix: version sync + pre-push checklist in github.md |
| v2.0.1 | 2026-05-10 | Fix: sync version history, add pre-push checklist |
| v2.0 | 2026-05-10 | Real-world impact data, before/after metrics, privacy audit |
| v1.9 | 2026-05-10 | INDEX cross-ref, combined triggers, knowledge cross-links |
| v1.8 | 2026-05-10 | Honest comparison: template vs memory service |

## License

MIT
