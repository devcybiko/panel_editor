#!/bin/bash
set -e  # Exit on first error

# Check if python3.13 exists
if ! command -v python3.13 &> /dev/null; then
    echo "Error: python3.13 not found"
    exit 1
fi

# Create venv
echo "Creating virtual environment..."
python3.13 -m venv .venv --clear

# Activate venv and upgrade pip
echo "Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

echo "✓ Installation complete!"
echo "Activate with: source .venv/bin/activate"