# Sowilo Frontend

React + TypeScript frontend for the Sowilo job opportunities tracker.

## Setup

### Prerequisites

- Node.js 18+
- npm

### Installation

1. **From monorepo root:**

   ```bash
   npm run install:frontend
   ```

2. **Or standalone:**
   ```bash
   cd frontend
   npm install
   ```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:

- `VITE_API_BASE_URL`: Backend API URL (default: http://localhost:8000)

## Running

### Development

**From monorepo root:**

```bash
npm run dev:frontend
```

**Or standalone:**

```bash
cd frontend
npm run dev
```

### Production Build

```bash
cd frontend
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── api/          # API client
│   ├── components/   # React components
│   ├── pages/        # Page components
│   ├── types/        # TypeScript types
│   ├── lib/          # Utilities
│   └── assets/       # Static assets
├── public/           # Public assets
├── package.json
├── .env.example
└── README.md
```

## Technologies

- React 18
- TypeScript
- Vite
- Tailwind CSS
- Shadcn/ui components
