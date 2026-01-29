#!/bin/bash
# Start LearnFlow backend services

echo "Starting LearnFlow backend services..."

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate  # For Linux/Mac
# For Windows: venv\Scripts\activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the backend API server
echo "Starting LearnFlow API server on port 8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo "LearnFlow backend services started successfully!"
echo "API available at: http://localhost:8000"
echo "API documentation available at: http://localhost:8000/docs"