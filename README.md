# 🧠 mem0-mcp

![Python Version](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

> A powerful [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server with [mem0](https://mem0.ai) integration for seamless coding knowledge management.

Store, search, and retrieve your coding patterns, snippets, and best practices through an elegant API that's compatible with Cursor, n8n, and other MCP clients.

## ✨ Features

-   🔍 **Semantic Search**: Find exactly what you need with powerful search capabilities
-   🔄 **Multiple Endpoints**: Support for MCP, SSE, and message-based communication
-   🌐 **CORS Support**: Built-in cross-origin resource sharing for web integrations
-   🐳 **Docker Ready**: Full containerization support with Docker and docker-compose
-   🔗 **ngrok Integration**: Expose your local server securely to the internet
-   🤖 **n8n Compatibility**: Seamless integration with n8n workflow automation

## 🚀 Quick Start

### Prerequisites

-   Python 3.12+
-   A mem0 API key ([get one here](https://mem0.ai))

### 💻 Local Installation

1. Clone this repository

```bash
git clone https://github.com/vonhatcuong/mem0-mcp.git
cd mem0-mcp
```

2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your mem0 API key

```bash
echo "MEM0_API_KEY=your_api_key_here" > .env
```

### 🐳 Docker Installation

1. Clone the repository and navigate to it

```bash
git clone https://github.com/vonhatcuong/mem0-mcp.git
cd mem0-mcp
```

2. Create a `.env` file with your credentials

```bash
cp .env.example .env
# Edit .env with your preferred text editor to add your MEM0_API_KEY
```

3. Build and start with Docker Compose

```bash
docker-compose up -d
```

## 🏃‍♂️ Running the Server

### Standard Mode

```bash
./run.sh
```

Or with custom host and port:

```bash
./run.sh --host 127.0.0.1 --port 9000
```

### With CORS Support (for n8n integration)

```bash
python main_with_cors.py
```

### With ngrok for Public Access

1. Make sure you have ngrok installed and configured:

```bash
# Install ngrok if needed
brew install ngrok  # On macOS with Homebrew

# Configure ngrok with your authtoken
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

2. Start the server with ngrok tunnel:

```bash
./start_ngrok.sh
```

## 📊 Usage Examples

### Using with Cursor

1. Start the server as described above
2. In Cursor, connect to the SSE endpoint:

```
http://localhost:8080/sse
```

3. Use the provided tools:
    - `add_coding_preference`: Store code snippets
    - `get_all_coding_preferences`: Retrieve all patterns
    - `search_coding_preferences`: Search for specific code

### Using with n8n

See our [detailed n8n integration guide](./n8n_integration_guide.md) for configuring n8n.vbi-server.com with mem0-mcp.

### API Endpoints

| Endpoint     | Method | Description                             |
| ------------ | ------ | --------------------------------------- |
| `/sse`       | GET    | SSE endpoint for MCP clients to connect |
| `/mcp`       | POST   | For handling direct MCP tool calls      |
| `/messages/` | POST   | Enhanced endpoint for n8n tool calls    |
| `/health`    | GET    | Health check endpoint                   |

## 📁 Project Structure

```
mem0-mcp/
├── 📄 .dockerignore        # Files to exclude from Docker builds
├── 📄 .env.example         # Template for environment variables
├── 📄 .gitignore           # Git ignore patterns
├── 📄 .python-version      # Python version specification
├── 📄 Dockerfile           # Docker container configuration
├── 📄 README.md            # Project documentation
├── 📄 docker-compose.yml   # Docker Compose configuration
├── 📄 main_with_cors.py    # Enhanced server with CORS for n8n
├── 📄 n8n_integration_guide.md # Guide for n8n integration
├── 📄 pyproject.toml       # Project configuration
├── 📄 requirements.txt     # Python dependencies
├── 📄 run.sh               # Convenience script to run standard server
├── 📄 start_ngrok.sh       # Script for ngrok tunnel creation
└── 📁 src/
    └── 📄 app.py           # Core server implementation
```

## ⚙️ Environment Variables

| Variable          | Description                                      | Default |
| ----------------- | ------------------------------------------------ | ------- |
| `MEM0_API_KEY`    | Your mem0 API key (required)                     | -       |
| `HOST`            | Host to bind the server to                       | 0.0.0.0 |
| `PORT`            | Port to bind the server to                       | 8080    |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed origins for CORS | \*      |
| `NGROK_AUTHTOKEN` | ngrok authentication token for tunneling         | -       |

## 🛠️ Development

### Requirements

-   Python 3.12+
-   Development tools:
    -   pytest for testing
    -   black for code formatting
    -   isort for import sorting

### Setup Development Environment

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Format code
black .
isort .
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
