#!/bin/bash
echo "Setting up Sowilo monorepo..."

# Backend setup
echo "Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Frontend setup
echo "Setting up frontend..."
cd frontend
npm install
cd ..

# Install root dependencies
echo "Installing root dependencies..."
npm install

echo "Setup complete! Run 'npm run dev' to start development."
