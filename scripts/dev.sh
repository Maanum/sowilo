#!/bin/bash

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend
echo "📡 Starting FastAPI backend..."
cd backend
source venv/bin/activate
python src/main.py &
BACKEND_PID=$!
cd ..

echo "[dev.sh] FastAPI backend started on port 8000 (PID $BACKEND_PID)"

# Start frontend
echo "🎨 Starting Vite frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "[dev.sh] Vite frontend started on port 5173 (PID $FRONTEND_PID)"

echo "[dev.sh] Both backend and frontend are running. Press Ctrl+C to stop."

# Wait for both to exit
wait $BACKEND_PID $FRONTEND_PID
