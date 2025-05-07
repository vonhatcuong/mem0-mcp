FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget unzip curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --upgrade pip && \
    pip install uv

# Create virtual environment
RUN python -m venv /app/.venv
# Set PATH to use python and pip from the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy configuration files and install dependencies in the virtual environment
COPY pyproject.toml .
RUN uv pip install -e .

# Install ngrok
RUN wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz && \
    tar xvzf ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin && \
    rm ngrok-v3-stable-linux-amd64.tgz

# Copy the entire application (except files in .dockerignore)
COPY . .

# Copy .env file into the container
COPY .env .

# Expose server port
EXPOSE 8080

# Create startup script
RUN echo '#!/bin/bash\n\
\n\
if [ -n "$NGROK_AUTHTOKEN" ]; then\n\
  echo "Configuring ngrok with authtoken..."\n\
  ngrok config add-authtoken $NGROK_AUTHTOKEN\n\
  \n\
  echo "Starting ngrok tunnel..."\n\
  nohup ngrok http 8080 --log=stdout > /app/ngrok.log 2>&1 &\n\
  \n\
  sleep 5\n\
  \n\
  NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o "https://[^\"]*")\n\
  if [ -n "$NGROK_URL" ]; then\n\
    echo "================================================================="\n\
    echo "🎉 NGROK TUNNEL CREATED SUCCESSFULLY!"\n\
    echo "================================================================="\n\
    echo "Ngrok URL: $NGROK_URL"\n\
    echo "Use this URL to connect from external services:"\n\
    echo "- SSE Endpoint: ${NGROK_URL}/sse"\n\
    echo "- Messages Endpoint: ${NGROK_URL}/messages/"\n\
    echo "================================================================="\n\
  else\n\
    echo "❌ Could not retrieve ngrok URL. Check /app/ngrok.log for details."\n\
  fi\n\
else\n\
  echo "⚠️ NGROK_AUTHTOKEN not configured. Ngrok tunnel will not be created."\n\
  echo "Server can only be accessed from local network via Docker IP."\n\
fi\n\
\n\
echo "Starting mem0-mcp server..."\n\
# Python will automatically be called from the virtual environment due to ENV PATH\n\
exec python main_with_cors.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Default command when container runs
CMD ["/app/start.sh"]
