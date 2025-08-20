# Sowilo Backend

FastAPI backend for the Sowilo job opportunities tracker.

## Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **From monorepo root:**

   ```bash
   npm run install:backend
   ```

2. **Or standalone:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for security
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `OPENAI_API_KEY`: OpenAI API key for job parsing

## Running

### Development

**From monorepo root:**

```bash
npm run dev:backend
```

**Or standalone:**

```bash
cd backend
source venv/bin/activate
python src/main.py
```

### Production

```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:

- API docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── src/
│   ├── api/           # OpenAI client
│   ├── config.py      # Configuration
│   ├── db/           # Database models and DAOs
│   ├── llm/          # LLM integration
│   ├── main.py       # FastAPI app
│   ├── models/       # SQLAlchemy models
│   ├── routes/       # API routes
│   ├── schemas.py    # Pydantic schemas
│   ├── services/     # Business logic
│   └── utils/        # Utilities
├── requirements.txt
├── .env.example
└── README.md
```
