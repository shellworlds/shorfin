#!/bin/bash
echo "Setting up Shorfin Quantum Dashboard..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r frontend/requirements.txt

# Check if src directory exists
if [ ! -d "src" ]; then
    echo "Error: src directory not found. Make sure you're in the project root."
    exit 1
fi

# Create necessary directories
mkdir -p frontend/static/uploads

echo "Setup complete!"
echo ""
echo "To run the dashboard:"
echo "  cd frontend && python app.py"
echo ""
echo "Then open: http://localhost:5000"
echo ""
echo "For production:"
echo "  cd frontend && waitress-serve --port=5000 app:app"
