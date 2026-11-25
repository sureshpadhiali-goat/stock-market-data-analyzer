# Next.js dashboard extension (future phase)

The Python engine and optional FastAPI service are included. A production-quality Next.js interface is intentionally left as a separate frontend phase so the Python project can first be tested and understood.

Suggested frontend:
- Next.js App Router + TypeScript
- Tailwind CSS for layout
- Plotly.js or lightweight-charts for charting
- Fetch `/analyze?ticker=...&start=...&end=...` from the FastAPI service
- Show latest close, period return, annualized volatility, and trend description
- Add a watchlist only after persistence (SQLite/PostgreSQL) is implemented

Suggested API development URL: `http://127.0.0.1:8000`
Do not expose a development API directly to the public internet. Add authentication, input limits, caching, logging and deployment controls before production use.
