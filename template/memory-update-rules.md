# Copy this section into your agent's system instructions (AGENTS.md / CLAUDE.md / .cursorrules)

## Memory System - Forced Update Rules (Critical: Same Priority as Security Redlines)

### End-of-session check (mandatory)
At the end of EVERY conversation, the agent MUST check:
- `memory/claude-like/recent.md` — pitfalls, decisions, knowledge from this session
- `memory/knowledge/` (relevant domain files) — new tools, config changes
- `memory/daily/YYYY-MM-DD.md` — what happened today
- `memory/context/pending.md` — unfinished items
- `memory/claude-like/triggers.md` — new trigger keywords

### Start-of-session check (complementary)
At the start of EVERY new session, the agent MUST check if the previous session left any memory updates pending. If so, fill them in immediately.

### Immediate logging (pitfalls & decisions)
When hitting a pitfall or making a decision during conversation, log it IMMEDIATELY to `memory/claude-like/recent.md`. Do NOT wait for session end.

These rules CANNOT be skipped. They are at the same priority level as security redlines.
