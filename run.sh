#!/bin/bash

# WebShield Scanner Startup Script

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if results directory exists
if [ ! -d "results" ]; then
    echo "Creating results directory..."
    mkdir -p results
fi

# Start the application
echo "Starting WebShield Scanner..."
python app.py