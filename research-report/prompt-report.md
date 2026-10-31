# gapgpt Research Report — Multiagent Injection Prompt

## Context for Agent Injection
You are a multiagent system operating under GitOps protocol (2PL leases, SSOT, isolated worktrees). This prompt contains compressed research findings from gapgpt project analysis (2026-10-25).

## Project State Summary
- **Repository**: `/home/hamid/Projects/gapgpt`
- **Architecture**: PostgreSQL (gapgpt_chats) + Metabase BI + pgvector semantic search
- **Services**: gapgpt-client, postgres, metabase (docker-compose)
- **Dashboard**: Custom Python HTTP server (port 5056) exposing chat APIs
- **Multiagent Protocol**: SSOT + TTL leases (120s) + Git worktree isolation

## Key Findings (Compressed)

### Active Data
- 211 chats, 900 messages, 16 subject groups
- 53% chats "unassigned" (111 chats) — needs categorization
- Peak activity: Oct 11, 19, 23 (3 sessions/day)
- 20 active days out of 31 in Oct 2026

### Risks
1. **Auth bottleneck**: ACCESS_TOKEN expires 2026-11-01, no auto-refresh
2. **Disk pressure**: pgvector on `/mnt/archive3` (tight)
3. **Error pattern**: 60% auth failures in dashboard.log
4. **Token budget**: 100 free tokens/month; ~5,000 used in this session

### Completed Work
- Knowledge Hub: pgvector TF-IDF (512-dim) hybrid search
- Chat Dashboard: Kanban + subject grouping + sync status
- Timeline: Monthly analysis with activity heatmaps
- Migration plan: SQLite mimocode.db → PostgreSQL (see plan 1792309319523)

## Required Actions (Next 30 days)
1. [ ] Token rotation + auto-refresh mechanism
2. [ ] Migration completion verification (row counts)
3. [ ] Chat re-classification (unassigned 111 → target <30)
4. [ ] Generative UI MVP (LLM → dashboard filter)
5. [ ] Organizational chatbot MVP (intent → API)

## Multiagent Task Decomposition
```json
{
  "tasks": [
    {"id": "TOKEN-001", "summary": "Implement token auto-refresh", "status": "TODO"},
    {"id": "MIG-002", "summary": "Verify SQLite→PG migration row counts", "status": "IN_PROGRESS"},
    {"id": "CAT-003", "summary": "Classify 111 unassigned chats", "status": "TODO"},
    {"id": "UI-004", "summary": "Generative UI MVP: NL → dashboard filter", "status": "TODO"},
    {"id": "BOT-005", "summary": "Org chatbot: intent parser → API calls", "status": "TODO"}
  ],
  "leases": {"TTL": 120, "owner": "auto-assigned"}
}
```

## Deployment Target
- Static HTML: `rm.adlr.ir/research-report/`
- Multiagent injection: Feed this prompt + JSON to new agent session

## Source References
- Local: README.md, KNOWLEDGE_HUB.md, chat-groups-report.json, llfs/chats/*.md, dashboard.py, dashboard.log
- External: Wikipedia (DevOps, GitOps, BI, Data Warehouse, Generative AI)
- Generated: 2026-10-25 | All 29 topics covered | HTML5 Reveal.js at reports/research-report.html
