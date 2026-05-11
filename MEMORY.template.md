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

## Forced Memory Update Rules (Critical - Do Not Skip)

Set these rules in your agent's system prompt (e.g. AGENTS.md / CLAUDE.md / .cursorrules).
They override all other behavior priorities.

### End-of-session check (mandatory)
At the end of EVERY conversation, the agent MUST check:
- claude-like/recent.md - today's pitfall, decisions, knowledge learned
- knowledge/ (relevant files) - new tools / config changes
- daily/YYYY-MM-DD.md - what happened today
- context/pending.md - unfinished items
- triggers.md - new trigger keywords

### Start-of-session check (complementary)
At the start of EVERY new session, the agent MUST check if the previous session left any memory updates pending. If so, fill them in immediately.

### Pitfall/immediate logging
When hitting a pitfall or making a decision during conversation, log it IMMEDIATELY. Do NOT wait for session end.

These rules are at the same priority level as security redlines. They CANNOT be skipped.
