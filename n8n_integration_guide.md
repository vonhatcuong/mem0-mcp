# n8n.vbi-server.com Integration Guide for mem0-mcp

This guide explains how to integrate the mem0-mcp server with [n8n](https://n8n.io/) workflow automation platform, specifically n8n.vbi-server.com, using ngrok tunnels for remote access.

## Overview

This document provides instructions on connecting n8n.vbi-server.com with your local mem0-mcp server through an ngrok tunnel.

## Installation and Configuration

### 1. Install ngrok

If you haven't already installed ngrok, you can do so using Homebrew:

```bash
brew install ngrok
```

### 2. Register and Configure ngrok

> **Important**: ngrok requires an account and authentication before use.

1. Register for an account at: https://dashboard.ngrok.com/signup

2. After registering, get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken

3. Configure ngrok with your authtoken:

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

Replace `YOUR_AUTH_TOKEN` with the token you received from the ngrok website.

### 3. Run the mem0-mcp Server with CORS Support

```bash
cd mem0-mcp
source .venv/bin/activate
python main_with_cors.py
```

### 4. Create an ngrok Tunnel to Your Local Server

Open a new terminal and run:

```bash
./mem0-mcp/start_ngrok.sh
```

After running, ngrok will create a public URL, for example:

```
Forwarding  https://xxxx-xx-xx-xxx-xx.ngrok-free.app -> http://localhost:8080
```

### 5. Configure n8n to Use the ngrok URL

#### 5.1 Important Endpoints

With the ngrok URL being `https://xxxx-xx-xx-xxx-xx.ngrok-free.app` (replace with your actual URL):

-   **SSE Endpoint**: `https://xxxx-xx-xx-xxx-xx.ngrok-free.app/sse`
-   **Messages Endpoint**: `https://xxxx-xx-xx-xxx-xx.ngrok-free.app/messages/`

#### 5.2 Available mem0-mcp Tools

The mem0-mcp server provides 3 tools:

1. **add_coding_preference**: Store code and programming patterns
2. **get_all_coding_preferences**: Retrieve all saved code snippets
3. **search_coding_preferences**: Search for relevant code snippets

#### 5.3 Configuring HTTP Requests in n8n

When creating an HTTP Request node in n8n, use the following templates:

**Connecting to SSE**:

-   URL: `https://xxxx-xx-xx-xxx-xx.ngrok-free.app/sse`
-   Method: `GET`
-   Headers:
    -   `Accept`: `text/event-stream`

**Calling add_coding_preference tool**:

-   URL: `https://xxxx-xx-xx-xxx-xx.ngrok-free.app/messages/`
-   Method: `POST`
-   Body:

```json
{
    "type": "tool_call",
    "tool_call": {
        "id": "add_preference_call",
        "function": {
            "name": "add_coding_preference",
            "arguments": {
                "text": "// Sample JavaScript code\nfunction calculateSum(a, b) {\n  return a + b;\n}"
            }
        }
    }
}
```

**Calling search_coding_preferences tool**:

-   URL: `https://xxxx-xx-xx-xxx-xx.ngrok-free.app/messages/`
-   Method: `POST`
-   Body:

```json
{
    "type": "tool_call",
    "tool_call": {
        "id": "search_call",
        "function": {
            "name": "search_coding_preferences",
            "arguments": {
                "query": "sum function"
            }
        }
    }
}
```

### 6. Important Notes

-   ngrok URLs change each time you restart (free version)
-   Register for ngrok Pro to get a static URL that doesn't change
-   ngrok tunnels automatically close after 2 hours of inactivity (free version)
-   Make sure to update the URL in your n8n configuration whenever the ngrok URL changes

## Troubleshooting

### ngrok Authentication Errors

If you encounter this error:

```
ERROR: authentication failed: Usage of ngrok requires a verified account and authtoken.
```

Make sure you have:

1. Registered for an account at https://dashboard.ngrok.com/signup
2. Retrieved your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
3. Configured ngrok with the command `ngrok config add-authtoken YOUR_AUTH_TOKEN`

### CORS Errors

If you encounter CORS errors, check that:

-   The mem0-mcp server is running with the `main_with_cors.py` file
-   Headers in the HTTP Request are set correctly

### Connection Errors

If you can't connect:

-   Verify the ngrok tunnel is still active
-   Ensure the mem0-mcp server is running
-   Check that the ngrok URL is being used correctly in your n8n configuration

## Example Workflows

### Auto-Store Code Snippets from GitHub

This workflow automatically stores code snippets from GitHub repositories:

1. **GitHub Trigger Node**: Triggers on new commits to a repository
2. **GitHub Node**: Fetches the content of changed files
3. **Function Node**: Extracts code snippets and metadata
4. **HTTP Request Node**: Sends the extracted code to the mem0-mcp server using the `add_coding_preference` tool

### Daily Code Digest

This workflow sends a daily digest of stored code snippets:

1. **Schedule Trigger Node**: Triggers daily at a specific time
2. **HTTP Request Node**: Gets all coding preferences
3. **Function Node**: Formats the snippets into a readable digest
4. **Email Node**: Sends the digest via email

## Resources

-   [n8n Documentation](https://docs.n8n.io/)
-   [HTTP Request Node Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
-   [JSON Node Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.json/)
-   [ngrok Documentation](https://ngrok.com/docs/)
