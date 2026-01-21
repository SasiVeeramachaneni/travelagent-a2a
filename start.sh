#!/bin/bash
# Startup script for AWS App Runner

# Install dependencies in the runtime container
pip3 install -r requirements.txt

# Start the application
exec python3 -m uvicorn app:app --host 0.0.0.0 --port 8080
