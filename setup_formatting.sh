#!/bin/bash

echo "🚀 Setting up auto-formatting for Python and TypeScript..."

# Install Python formatting tools
echo "📦 Installing Python formatting tools..."
cd backend
pip install black flake8 mypy isort

# Install frontend formatting tools
echo "📦 Installing frontend formatting tools..."
cd ../frontend
npm install --save-dev prettier

echo "✅ Formatting tools installed!"
echo ""
echo "📝 Next steps:"
echo "1. Install recommended VS Code extensions (they should be prompted automatically)"
echo "2. Restart VS Code to apply settings"
echo "3. Format on save should now work automatically"
echo ""
echo "🔧 Manual formatting commands:"
echo "  Backend (from backend/ directory):"
echo "    black .                    # Format Python files"
echo "    isort .                    # Sort imports"
echo "    flake8 .                   # Lint Python files"
echo "    mypy .                     # Type check Python files"
echo ""
echo "  Frontend (from frontend/ directory):"
echo "    npx prettier --write .     # Format TypeScript/JavaScript files"
echo ""
echo "🎯 Auto-formatting is now configured to run on save!" 