# AI Agent Memory Template

> A structured, hierarchical memory system for AI agents, inspired by [memU](https://github.com/NevaMind-AI/MemU) (Memory as File System) and [Claude Code](https://code.claude.com/docs/zh-CN/memory) (Auto-memory + Trigger-based knowledge retrieval).

## Why this exists

AI agents forget everything between sessions. This template gives them a **file-based memory system** that survives restarts:

- **Knowledge** — domain expertise organized by topic, read on demand
- **Decisions** — irreversible choices with rationale (don't repeat mistakes)
- **Context** — what's pending, what's blocked, what's currently known
- **Auto-learning** — a rolling cache of recently learned lessons and corrections
- **Emotional memory** — relationship, rapport, user preferences (optional)

## Structure

```
memory/
├── claude-like/           ← Auto-learning (inspired by Claude Code)
│   ├── recent.md          ← Rolling 200-line cache of corrections & lessons
│   └── triggers.md        ← Keyword → knowledge file mapping
│
├── knowledge/             ← Domain expertise, read on demand
│   ├── git.md
│   ├── wsl.md
│   ├── proxy.md
│   ├── your-topic.md      ← Add as needed
│   └── ...
│
├── decisions/             ← Irreversible decisions with rationale
│   └── YYYY-MM-DD-topic.md
│
├── context/               ← Current state
│   ├── pending.md         ← Todo list
│   └── limitations.md     ← Known hard constraints
│
├── bonds/                 ← Emotional memory (relationship, rapport)
│   ├── profile.md         ← User personality & working style
│   ├── story.md           ← Shared history, milestones
│   └── vibe.md            ← Rapport, signals, unwritten rules
│
├── preferences/           ← User preferences
│   └── user.md
│
└── daily/                 ← Raw daily logs
    └── YYYY-MM-DD.md
```

## How it works

### For AI agents

Place a `MEMORY.md` file at your agent's workspace root with a navigation section pointing to the memory directory. The agent reads it at session start:

```
## Memory Navigation
- Lessons learned → memory/claude-like/recent.md (auto-load)
- Domain knowledge → memory/knowledge/ (trigger-based lookup)
- Pending tasks → memory/context/pending.md
- Known limits → memory/context/limitations.md
```

### Auto-learning workflow

1. **Agent is corrected** → immediately appends to `claude-like/recent.md`
2. **Agent starts a session** → reads `recent.md` first (capped at 200 lines)
3. **Over 200 lines** → oldest entries are distilled into `knowledge/` and removed
4. **Keyword triggers** → when conversation mentions "git", agent auto-reads `knowledge/git.md`

### Inspired by

| Source | What we borrowed |
|--------|-----------------|
| [memU](https://github.com/NevaMind-AI/memU) | Memory as hierarchical file system (categories/facts like folders/files) |
| [Claude Code Memory](https://code.claude.com/docs/zh-CN/memory) | Auto-learning cache, bounded context (200 lines), separate knowledge vs memory |
| [Claude Code Best Practices](https://code.claude.com/docs/zh-CN/best-practices) | Trigger-based retrieval, "correct → log → apply" loop |

## License

MIT
