# Sowilo Backend (FastAPI)

A modular FastAPI backend for tracking job opportunities, with LLM enrichment, HTML parsing, and .env-based config.

---

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env  # Edit as needed
   ```
2. **Start the server:**
   ```bash
   uvicorn backend.main:app --reload
   # or from project root:
   ./dev.sh
   ```
3. **API docs:** http://localhost:8000/docs

---

## 🗂️ Structure

- `main.py` — FastAPI entrypoint
- `config.py` — Loads .env and settings
- `models/` — SQLAlchemy models
- `db/` — DB base, session, DAOs
- `routes/` — APIRouters
- `services/` — Business logic
- `llm/` — LLM, scraping, enrichment
- `.env.example` — Example config

---

## 🔑 Environment Variables
- All config is via `.env` (see `.env.example`)
- **Never commit real secrets!**

---

## 🔧 Features
- Modular, domain-driven structure
- CRUD + enrichment endpoints (including `/opportunities/from-link`)
- LLM integration (OpenAI, GPT, etc.)
- HTML parsing (BeautifulSoup, Playwright ready)
- CORS for frontend integration
- Auto-generated API docs

---

## 🧪 Dev & Tools
- **Playwright**: For browser automation/scraping
- **BeautifulSoup**: For HTML parsing
- **OpenAI**: For LLM enrichment (set `OPENAI_API_KEY` in `.env`)
- **dev.sh**: Starts both backend and frontend in parallel for development

---

## 📚 Documentation
- API docs: http://localhost:8000/docs
- See main project README for full-stack info

---

## License
MIT (or your choice) 