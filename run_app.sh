#!/bin/bash

# Sign Language Detection Application Launcher
# This script helps you run the application with proper setup

echo "=========================================="
echo "Sign Language Detection Application"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "No virtual environment found. Creating one..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python3 -c "import cv2" 2>/dev/null; then
    echo ""
    echo "Dependencies not installed. Installing..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Check for model file
echo ""
echo "Checking for model file..."
MODEL_FOUND=0
for model in model.h5 model.keras asl_model.h5 sign_language_model.h5; do
    if [ -f "$model" ]; then
        echo "✓ Model found: $model"
        MODEL_FOUND=1
        break
    fi
done

if [ $MODEL_FOUND -eq 0 ]; then
    echo "⚠ Warning: No model file found!"
    echo "Please place your trained model (.h5 or .keras) in this directory"
    echo "Or update MODEL_PATH in config.py"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run the application
echo ""
echo "=========================================="
echo "Starting application..."
echo "=========================================="
echo ""

python3 sign_language_app.py

# Deactivate virtual environment
deactivate
