#!/bin/bash

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📥 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Start FastAPI backend
echo "📡 Starting FastAPI backend..."
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