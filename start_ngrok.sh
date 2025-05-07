#!/bin/bash
# Script to start an ngrok tunnel for the mem0-mcp server
# Usage: ./start_ngrok.sh [port] [authtoken]

# Default port if not specified
PORT=${1:-8080}
# Default to environment variable or empty string if not provided
NGROK_AUTHTOKEN=${2:-$NGROK_AUTHTOKEN}

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ Error: ngrok is not installed. Please install it from https://ngrok.com/download"
    exit 1
fi

# Check if authtoken is provided
if [ -z "$NGROK_AUTHTOKEN" ]; then
    echo "⚠️ Warning: NGROK_AUTHTOKEN not provided."
    echo "You can get a free authtoken from https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "Usage: ./start_ngrok.sh [port] [authtoken]"
    echo "  or set NGROK_AUTHTOKEN in your environment"
    echo ""
    echo "⚠️ Operating without an authtoken will limit your connection time."
    read -p "Do you want to continue without an authtoken? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    # Configure ngrok with the provided authtoken
    echo "🔑 Configuring ngrok with authtoken..."
    ngrok config add-authtoken $NGROK_AUTHTOKEN
fi

# Start ngrok
echo "🚀 Starting ngrok tunnel on port $PORT..."
ngrok http $PORT --log=stdout
