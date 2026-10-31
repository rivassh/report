# CONSTITUTION.md — gapgpt Reporting Rules

## Rule 1: Connection Tracking After Every Message

After EVERY response/message, append a "Known Connections & Last Sync" table at the very end.

**Template:**
```
## 🔗 اتصالات فعال و آخرین همگام‌سازی

| اتصال | نوع | آخرین همگام‌سازی | وضعیت |
|-------|-----|------------------|--------|
| gapgpt.app API | REST (Cookies + ACCESS_TOKEN) | <timestamp> | <active/stale/unknown> |
| PostgreSQL gapgpt_chats | Docker DB (port 5435) | <timestamp> | <active/stale/unknown> |
| pgvector | pgvector/pgvector:pg16 (port 5436) | <timestamp> | <active/stale/unknown> |
| OpenRouter ai.adlr.ir/api/v1 | LLM proxy | <timestamp> | <active/down/unknown> |
| llfs/ | Local filesystem | <timestamp> | <active/stale/unknown> |
| mimocode سرور | Remote SQLite (3 sources merged) | <timestamp> | <active/stale/unknown> |
```

**Verification commands:**
- gapgpt.app: `curl -s -o /dev/null -w "%{http_code}" https://gapgpt.app/api/v1/chat_list?offset=0&limit=1`
- PostgreSQL: `docker exec gapgpt-postgres psql -U gapgpt -d gapgpt_chats -c "SELECT count(*) FROM chats;"`
- pgvector: `docker exec gapgpt-pgvector psql -U postgres -d gapgpt_vectors -c "SELECT count(*) FROM vectors;"`
- OpenRouter: `curl -s -o /dev/null -w "%{http_code}" https://ai.adlr.ir/api/v1/health`

---

## Rule 2: Report Scale — Not "Small"

The report must visibly demonstrate scale:
- 211 chats, 900 messages, 16 subject groups
- 29 topics, each with local data + external citation + cross-verification
- Activity timeline with peaks/gaps
- Error patterns (401 auth failures dominate logs)
- 30-day roadmap with owners and deadlines

---

## Rule 3: Data Persistence

All editable report data MUST be saved to `reports/research-report-data.json` before any HTML regeneration.

---

## Rule 4: Token Expiry Deadline

ACCESS_TOKEN expires **2026-11-01**. All sync infrastructure must have auto-refresh before this date.

---

## Rule 5: SIMA vs gapgpt Distinction

These reports cover gapgpt only. SIMA (`/opt/ymls/sima`) is a separate project with:
- Different Docker stack
- Different token system (OpenRouter proxy, not ACCESS_TOKEN)
- Different task IDs (TASK-040+ vs TOKEN-001+)
- Different API endpoints

Never mix SIMA data into gapgpt reports without explicit labeling.
