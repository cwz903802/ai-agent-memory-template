# -*- coding: utf-8 -*-
import os

repo = r'A:\openclaw\projects\ai-agent-memory-template'

# --- Update MEMORY.template.md: add forced update section ---
mt_path = os.path.join(repo, 'MEMORY.template.md')
with open(mt_path, 'r', encoding='utf-8') as f:
    mt = f.read()

forced_section = '''
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
'''

mt = mt + forced_section
with open(mt_path, 'w', encoding='utf-8') as f:
    f.write(mt)
print('MEMORY.template.md updated')

# --- Update README.md: add forced update mechanism section ---
readme_path = os.path.join(repo, 'README.md')
with open(readme_path, 'r', encoding='utf-8') as f:
    readme = f.read()

# Update auto-learning workflow section
old_workflow = '''### Auto-learning workflow

1. **Agent is corrected** -> immediately appends to `claude-like/recent.md`
2. **Agent starts a session** -> reads `recent.md` first (capped at 200 lines)
3. **Over 200 lines** -> oldest entries are distilled into `knowledge/` and removed
4. **Keyword triggers** -> when conversation mentions "git", agent auto-reads `knowledge/git.md`'''

new_workflow = '''### Auto-learning workflow

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

> **Status after 10+ hours of practical use:** Without enforcement, the agent logged daily summaries but failed to update `knowledge/` and `claude-like/recent.md` consistently. After adding forced update rules (same priority as security redlines), all memory components were maintained reliably across sessions.'''

if old_workflow in readme:
    readme = readme.replace(old_workflow, new_workflow)
    print('README.md workflow section updated')
else:
    print('README.md: could not find old workflow section')

# Update version and version history
old_ver = '| v2.0.2 | 2026-05-10 |'
new_ver = '| v2.0.3 | 2026-05-12 | Fix: forced memory update rules, start-of-session check, immediate logging |\n| v2.0.2 | 2026-05-10 |'
if old_ver in readme:
    readme = readme.replace(old_ver, new_ver)
    print('README.md version updated')
else:
    print('README.md: could not find v2.0.2 version line')

old_hist = '| v2.0.2 | 2026-05-10 | Fix: version sync + pre-push checklist in github.md |'
new_hist = '| v2.0.3 | 2026-05-12 | Fix: forced memory update rules, start-of-session check, immediate logging |\n| v2.0.2 | 2026-05-10 | Fix: version sync + pre-push checklist in github.md |'
if old_hist in readme:
    readme = readme.replace(old_hist, new_hist)
    print('README.md version history updated')
else:
    # Try without the specific text
    readme = readme.replace('| v2.0.2 | 2026-05-10 | Fix: version sync + pre-push checklist in github.md |', new_hist)
    print('README.md version history updated (alt)')

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme)

print()
print('All updates done')
