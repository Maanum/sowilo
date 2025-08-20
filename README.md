# Sowilo - Job Opportunities Tracker

A modern job opportunities tracker built with FastAPI backend and React frontend, organized as a monorepo for efficient development and deployment.

## 🏗️ Monorepo Structure

```
sowilo/
├── backend/           # FastAPI Python backend
│   ├── src/          # Python source code
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/          # React TypeScript frontend
│   ├── src/          # React source code
│   ├── package.json
│   ├── .env.example
│   └── README.md
├── scripts/           # Development scripts
├── .cursor/           # IDE configuration
├── package.json       # Root orchestration
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.8+
- npm

### Setup

1. **Clone and setup:**

   ```bash
   git clone <repository-url>
   cd sowilo
   npm run setup
   ```

2. **Or use the setup script:**

   ```bash
   ./scripts/setup.sh
   ```

3. **Start development:**
   ```bash
   npm run dev
   ```

## 🛠️ Development

### Running Services

**Both services together:**

```bash
npm run dev
```

**Backend only:**

```bash
npm run dev:backend
```

**Frontend only:**

```bash
npm run dev:frontend
```

**Or use the dev script:**

```bash
./scripts/dev.sh
```

### Service URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📦 Service Independence

Each service can be developed and deployed independently:

### Backend (FastAPI)

- **Location**: `./backend/`
- **Entry point**: `backend/src/main.py`
- **Dependencies**: `backend/requirements.txt`
- **Environment**: `backend/.env`

### Frontend (React)

- **Location**: `./frontend/`
- **Entry point**: `frontend/src/main.tsx`
- **Dependencies**: `frontend/package.json`
- **Environment**: `frontend/.env`

## 🔧 Available Scripts

### Root Level

- `npm run dev` - Start both services
- `npm run setup` - Install all dependencies
- `npm run install` - Install all dependencies
- `npm run lint` - Lint frontend code

### Backend

- `npm run dev:backend` - Start backend only
- `npm run install:backend` - Install Python dependencies

### Frontend

- `npm run dev:frontend` - Start frontend only
- `npm run install:frontend` - Install Node dependencies
- `npm run lint:frontend` - Lint frontend code
- `npm run type-check` - TypeScript type checking

## 🌍 Environment Configuration

### Backend Environment

Copy `backend/.env.example` to `backend/.env`:

```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

### Frontend Environment

Copy `frontend/.env.example` to `frontend/.env`:

```bash
cd frontend
cp .env.example .env
# Edit .env with your configuration
```

## 🚀 Deployment

Each service can be deployed independently:

### Backend Deployment

```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Frontend Deployment

```bash
cd frontend
npm run build
# Deploy the dist/ folder to your hosting service
```

## 📚 Documentation

- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)
- [API Documentation](http://localhost:8000/docs) (when running)

## 🛠️ Development Workflow

1. **Feature Development**: Work in the appropriate service directory
2. **Testing**: Each service can be tested independently
3. **Integration**: Use `npm run dev` to test full-stack integration
4. **Deployment**: Deploy services separately or together

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes in the appropriate service directory
4. Test both services independently and together
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details
