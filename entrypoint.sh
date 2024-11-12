#!/bin/bash
set -e

if [ "$1" = "batch-vectorize" ]; then
    echo "Running batch vectorization..."
    python src/vectorization/vectorize_data.py
else
    echo "Starting main application..."
    exec uvicorn src.main:app --host 0.0.0.0 --port 8000
fi
