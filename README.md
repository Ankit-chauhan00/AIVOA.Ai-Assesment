# CRM Assessment — Tools & HCP Management (OPM)

Brief overview of the codebase, toolchain, and the HCP Management Operational Process Model (OPM).

## Project layout

- `crm-backend/`: FastAPI backend and database models.
- `crm-frontend/`: React + Vite frontend.

## Tooling / What this project uses

- Python 3.10+ (check `pyproject.toml` in `crm-backend/`).
- FastAPI — backend web framework (ASGI).
- Uvicorn — ASGI server used for local development.
- SQLAlchemy — ORM for database models.
- Alembic — DB migrations.
- Pydantic — request/response schemas.
- React + Vite — frontend application.
- npm / Node.js — frontend package manager and tooling.

## How to run (local dev)

Backend (from `crm-backend/`):

```bash
cd crm-backend
# run migrations (if configured)
alembic upgrade head
# run backend (reload for development)
uv run uvicorn app:main:app --reload
```

Frontend (from `crm-frontend/`):

```bash
cd crm-frontend
npm install
npm run dev
```

## HCP Management — Operational Process Model (OPM)

Purpose: manage Healthcare Professional (HCP) records, record interactions, and track follow-ups.

Primary responsibilities:

- Create and update HCP profiles (contact, specialty, organization).
- Log interactions between agents and HCPs, with timestamps and summaries.
- Schedule and track follow-ups (reminders, statuses).
- Provide APIs for searching, filtering and exporting HCP data.

Suggested API surface (examples)

- `GET /hcp` — list HCPs (with filters, pagination).
- `POST /hcp` — create HCP profile.
- `GET /hcp/{id}` — retrieve profile + recent interactions.
- `PUT /hcp/{id}` — update profile.
- `POST /hcp/{id}/interactions` — log an interaction.
- `GET /interactions` — list interactions (filter by HCP, date, agent).
- `POST /followups` — create follow-up tasks.

Data & workflows

- HCP profile: identification, contact, specialty, organization, notes.
- Interaction record: who, when, medium, summary, next steps.
- Follow-up: linked to HCP and/or interaction; has due date and status.

Operational notes

- Keep interaction summaries concise and structured (objective, outcome, next step).
- Use follow-ups to drive a queue of outreach tasks; surface overdue items in the UI.
- Record minimal sensitive data; follow privacy and compliance rules for real deployments.

## Contributing / Next steps

- Add or update OpenAPI docs (FastAPI auto-generates schema at `/docs`).
- Add migrations and seed data to exercise HCP flows.
- Implement frontend screens for listing, editing HCPs and logging interactions.

## Useful files

- Backend entry: `crm-backend/app/main.py` — application startup.
- Backend models: `crm-backend/app/models/` — HCP and interaction models.
- Frontend entry: `crm-frontend/src/main.jsx` — React root.

---

If you want, I can also add example API requests, seed data, or wire up a simple HCP CRUD UI.
