# Sowilo: Job Opportunities Tracker

A full-stack monorepo for tracking job opportunities, built with FastAPI (Python) and React (TypeScript).

---

## 🏗️ Project Structure

```
sowilo/
├── backend/           # FastAPI backend (modular, .env support)
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── models/
│   ├── db/
│   ├── routes/
│   ├── services/
│   └── llm/
├── frontend/          # React + Vite + Tailwind + shadcn/ui
│   ├── src/
│   ├── node_modules/
│   └── package.json
├── dev.sh             # Start both backend and frontend in dev mode
├── start.sh           # (Optional) Start both for local prod
└── .gitignore         # Ignores venv, node_modules, .env, etc.
```

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit as needed
```

- Start backend (from project root):
  ```bash
  uvicorn backend.main:app --reload
  # or
  ./dev.sh
  ```
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
- App: http://localhost:5173

---

## 🛠️ Features

### Backend (FastAPI)
- Modular, domain-driven structure (models, db, services, routes, llm)
- Environment config via `.env` (see `.env.example`)
- SQLite (default), but supports any SQLAlchemy DB
- CRUD + enrichment endpoints (including `/opportunities/from-link`)
- LLM integration (OpenAI, GPT, etc.)
- HTML parsing (BeautifulSoup, Playwright ready)
- CORS for frontend integration
- Auto-generated API docs

### Frontend (React + Vite)
- Modern React 18 + TypeScript
- Tailwind CSS + shadcn/ui for beautiful UI
- Dark mode toggle
- Responsive, mobile-first design
- Add opportunities via URL (enrichment) or manual entry
- Axios for API calls

---

## 🔧 API Endpoints (Key)
- `GET /opportunities` — List all opportunities
- `POST /opportunities` — Create a new opportunity (manual)
- `POST /opportunities/from-link` — Create from job posting URL (enrichment)
- `DELETE /opportunities/{id}` — Delete an opportunity

---

## 📊 Data Model
- `title` (required)
- `company` (required)
- `level`, `min_salary`, `max_salary`, `posting_link`, `resume_link`, `cover_letter_link`, `status` (optional)

---

## 🔒 Environment & Secrets
- All backend config is via `.env` (see `backend/.env.example`)
- **Never commit real secrets!**
- Add `.env` to your `.gitignore` (already done)

---

## 🧪 Testing & Dev Tools
- **Playwright**: For browser automation/scraping (see backend requirements)
- **BeautifulSoup**: For HTML parsing
- **OpenAI**: For LLM enrichment (set `OPENAI_API_KEY` in `.env`)
- **dev.sh**: Starts both backend and frontend in parallel for development

---

## 📝 Contributing & Next Steps
- Add more LLM enrichers or scraping logic
- Add user authentication
- Add search/filtering, status tracking, etc.
- Add tests in `backend/tests/` and `frontend/src/__tests__/`

---

## 📚 Documentation
- Backend: http://localhost:8000/docs
- Frontend: See code and README in `frontend/`

---

## License
MIT (or your choice) 