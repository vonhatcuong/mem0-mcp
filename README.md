# mem0-mcp: MCP Server for Managing Coding Preferences

This is a clean implementation of an [MCP](https://modelcontextprotocol.io/introduction) server with [mem0](https://mem0.ai) integration for efficiently managing coding preferences. The server provides a structured approach to store, retrieve, and search coding patterns through MCP-compatible tools.

## Features

-   Store code snippets with comprehensive context
-   Retrieve and search coding preferences using semantic search
-   Cross-origin resource sharing (CORS) support
-   Compatible with Cursor and other MCP clients

## Quick Start

### Prerequisites

-   Python 3.8+
-   A mem0 API key ([get one here](https://mem0.ai))

### Installation

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

### Running the Server

```bash
./run.sh
```

Or with custom host and port:

```bash
./run.sh --host 127.0.0.1 --port 9000
```

## Usage with Cursor

1. Start the MCP server as described above
2. In Cursor, connect to the SSE endpoint:

```
http://localhost:8080/sse
```

3. Use the provided tools to manage your coding preferences:
    - `add_coding_preference`: Store code snippets with context
    - `get_all_coding_preferences`: Retrieve all stored coding patterns
    - `search_coding_preferences`: Find specific coding preferences

## Project Structure

```
mem0-mcp/
├── .env.example         # Template for environment variables
├── .gitignore           # Git ignore patterns
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
├── run.sh               # Convenience script to run the server
└── src/
    └── app.py           # Main application code
```

## Environment Variables

-   `MEM0_API_KEY`: Your mem0 API key (required)
-   `HOST`: Host to bind the server to (default: 0.0.0.0)
-   `PORT`: Port to bind the server to (default: 8080)
-   `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS (default: \*)

## License

MIT
