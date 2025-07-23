# Sowilo Frontend

A modern React TypeScript frontend for the Job Opportunities Tracker, built with Vite, Tailwind CSS, and shadcn/ui.

---

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```
2. **Start the dev server:**
   ```bash
   npm run dev
   # or from project root:
   ./dev.sh
   ```
3. **App:** http://localhost:5173

---

## 🛠️ Features
- Modern React 18 + TypeScript
- Tailwind CSS + shadcn/ui for beautiful UI
- Dark mode toggle
- Responsive, mobile-first design
- Add opportunities via URL (enrichment) or manual entry
- Axios for API calls

---

## ✨ Components
- **Button** — shadcn/ui
- **Card** — shadcn/ui
- **Input** — shadcn/ui
- **Label** — shadcn/ui
- **Dialog** — shadcn/ui
- **Lucide React** — Icon library

---

## 🌙 Dark Mode
- Toggle in header
- Persists user preference in localStorage
- Respects system preference on first visit

---

## 🔗 API Integration
- Connects to FastAPI backend at http://localhost:8000
- Add opportunities via `/opportunities` (manual) or `/opportunities/from-link` (URL enrichment)

---

## 📝 Development
- Hot reload (Vite)
- TypeScript + ESLint
- Path aliases (`@/` for `src/`)

---

## 🚀 Build
To build for production:
```bash
npm run build
```
To preview the production build:
```bash
npm run preview
```

---

## License
MIT (or your choice)
