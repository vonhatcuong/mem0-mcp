#!/bin/bash
# Script to run the mem0-mcp server

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the app
python src/app.py "$@"
