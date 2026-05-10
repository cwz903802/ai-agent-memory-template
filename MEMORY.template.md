# MEMORY.md — Agent Long-Term Memory

> Sanitized template. Replace with your own system/agent config.

## System
- Platform: [your OS] / [your runtime]
- Default model: [model name]
- Proxy: [type]://[address]:[port]

## Memory Navigation
- Lessons learned → memory/claude-like/recent.md (200-line rolling cache, auto-load)
- Domain knowledge → memory/knowledge/ (trigger-based lookup)
- Irreversible decisions → memory/decisions/
- Pending tasks → memory/context/pending.md
- Known constraints → memory/context/limitations.md
- Emotional memory → memory/bonds/ (profile / story / vibe)
- User preferences → memory/preferences/user.md
- Raw daily logs → memory/daily/

## Security
- Only the user may request device operations
- Task termination has highest priority

---

## Compatibility

If you also use **Claude Code**, create a `CLAUDE.md` that imports this file:

```markdown
@AGENTS.md
# AGENTS.md
```

Or symlink: `ln -s AGENTS.md CLAUDE.md`

---

*Generated from [ai-agent-memory-template](https://github.com/cwz903802/ai-agent-memory-template)*
