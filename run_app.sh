#!/bin/bash

# Entertainment Suggester Launcher Script
# This script checks dependencies and starts the application

echo "Starting Entertainment Suggester..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not installed or not in PATH"
        echo "Please install Python 3.8+ from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "Using Python $PYTHON_VERSION"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! $PYTHON_CMD -c "import PyQt6" &> /dev/null; then
    echo "Installing dependencies..."
    $PYTHON_CMD -m pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        echo "Please run: $PYTHON_CMD -m pip install -r requirements.txt"
        exit 1
    fi
fi

# Check TMDB API configuration
if grep -q "YOUR_TMDB_API_KEY_HERE" config.py; then
    echo
    echo "⚠️  TMDB API key not configured!"
    echo "For the best experience, get a free API key from:"
    echo "https://www.themoviedb.org/settings/api"
    echo "Then edit config.py and replace YOUR_TMDB_API_KEY_HERE with your key."
    echo
    echo "The app will work without an API key, but with limited features."
    echo
fi

# Run the application
echo "Starting application..."
$PYTHON_CMD main.py

if [ $? -ne 0 ]; then
    echo
    echo "Application exited with an error."
    echo "Check the error messages above for troubleshooting."
fi