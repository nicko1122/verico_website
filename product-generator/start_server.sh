#!/bin/bash
# This script starts the Product Generator web server.
# It ensures dependencies are installed within a virtual environment.

# Navigate to the script's own directory to ensure correct paths
cd "$(dirname "$0")"

echo "--- Setting up Product Generator Server ---"

# Check for a virtual environment
if [ ! -d "venv" ]; then
    echo "Python virtual environment not found. Creating one..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please ensure python3 and venv are installed."
        exit 1
    fi
fi

# Activate the virtual environment
source venv/bin/activate

# Check for a flag file to see if dependencies were already installed
if [ ! -f "venv/installed.flag" ]; then
    echo "Installing/updating dependencies from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies."
        deactivate
        exit 1
    fi
    # Create a flag file to skip installation next time
    touch venv/installed.flag
else
    echo "Dependencies already installed. Skipping installation."
fi

echo "--- Starting Flask Server ---"
echo "Access the uploader at http://0.0.0.0:5001"
echo "Press Ctrl+C to stop the server."

# Start the server
python server.py

# Deactivate venv when server is stopped
deactivate
echo "--- Server stopped. Virtual environment deactivated. ---"

