#!/bin/bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org