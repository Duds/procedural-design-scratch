#!/bin/bash
# Start Jupyter Lab with the virtual environment activated

cd "$(dirname "$0")"
source venv/bin/activate
jupyter lab

