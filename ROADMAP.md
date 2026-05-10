# Roadmap

Known limitations and planned improvements for the file-based memory approach.

## Known Limitations

### 1. Manual Knowledge Retrieval
Knowledge files are read on-demand — the agent must remember to check them. A trigger-word system (`triggers.md`) helps but is not automatic.

**Planned:** Convert knowledge files into platform-specific skill formats (OpenClaw `skills/*/SKILL.md`, Claude Code `.claude/rules/*.md`, etc.) for automatic context-matching.

### 2. Manual Learning Logging
When the agent is corrected, it must manually append to `recent.md`. There's no automatic detection of correction patterns.

**Planned:** Define a clear "correction → log" protocol that can be consistently followed. The 200-line cap forces periodic distillation.

### 3. No Cross-Session Statistics
The system doesn't track how often corrections happen, which knowledge files are most used, or consolidation frequency.

**Planned:** Add lightweight usage metrics to `context/stats.md` (optional, opt-in).

### 4. Single-Agent Design
The memory system is designed for one persistent agent. Temporary swarm workers (ClawTeam, agent teams) are intentionally stateless — they receive task-specific context at spawn time and don't accumulate memory.

**This is by design.** Workers are ephemeral. Only the coordinator needs long-term memory.

### 5. Token Cost of Auto-Learning
`recent.md` is loaded every session (~200 lines, ~3k tokens). This is the insurance premium for cross-session continuity. Without it, the agent starts blank every time.

## Future Directions

### v2.0 — Hybrid Skill Integration
- Auto-convert `knowledge/` files into platform-specific skill bundles
- Support OpenClaw skills, Claude Code rules, Cline rules simultaneously
- One `knowledge/` entry → auto-generate skill file for target platform

### v2.1 — Auto-Consolidation Trigger
- When `recent.md` reaches 180 lines, auto-initiate a consolidation pass
- Deduplicate, merge, and archive to `knowledge/`
- Keep `recent.md` under 200 lines

### v2.2 — Per-Project Memory
- `context/` scoped to projects (e.g., `context/project-xyz/pending.md`)
- Coordinator agent loads global memory + project-specific memory
- Workers remain stateless

## Version History

| Version | Date | Notes |
|---------|------|-------|
| v1.4 | 2026-05-10 | README: add ROADMAP reference |
| v1.3 | 2026-05-10 | Add ROADMAP.md |
| v1.2 | 2026-05-10 | Add applicability guide: per-agent/OS support |
| v1.1 | 2026-05-10 | Add version history table |
| v1.0 | 2026-05-10 | Initial release |
