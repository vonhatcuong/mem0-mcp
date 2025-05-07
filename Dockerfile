FROM python:3.10-slim

WORKDIR /app

# Install base dependencies including curl for healthcheck and ngrok
RUN apt-get update && apt-get install -y curl unzip && \
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install -y ngrok && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml .
COPY requirements.txt .
COPY .env.example .env
COPY src/ ./src/
COPY run.sh .

# Create a startup script that handles ngrok
RUN echo '#!/bin/bash\n\
# Start ngrok in the background if auth token is provided\n\
if [ -n "$NGROK_AUTHTOKEN" ]; then\n\
  echo "Starting ngrok tunnel..."\n\
  ngrok config add-authtoken $NGROK_AUTHTOKEN\n\
  ngrok http $PORT --log=stdout > /dev/null &\n\
  echo "Ngrok started. Web interface available at http://localhost:4040"\n\
fi\n\
\n\
# Start the application\n\
./run.sh\n\
' > /app/start.sh && chmod +x /app/start.sh

# Make run script executable
RUN chmod +x run.sh

# Install project dependencies
RUN uv pip install --system -r requirements.txt

# Expose the ports:
# - 8080: Main application port
# - 4040: Ngrok web interface port
EXPOSE 8080 4040

# Command to run the server with optional ngrok tunnel
CMD ["/app/start.sh"]
