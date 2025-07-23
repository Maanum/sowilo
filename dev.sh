#!/bin/bash

# Start FastAPI backend
uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!

echo "[dev.sh] FastAPI backend started on port 8000 (PID $BACKEND_PID)"

# Start Vite frontend
echo "[dev.sh] Starting Vite frontend on port 5173..."
cd frontend && npm run dev &
FRONTEND_PID=$!
cd ..

echo "[dev.sh] Vite frontend started on port 5173 (PID $FRONTEND_PID)"

echo "[dev.sh] Both backend and frontend are running. Press Ctrl+C to stop."

# Wait for both to exit
wait $BACKEND_PID $FRONTEND_PID 