# mem0-mcp Integration Guide for n8n

This guide explains how to integrate the mem0-mcp server with [n8n](https://n8n.io/) workflow automation platform. Using n8n, you can create automated workflows that interact with your mem0-mcp server to store, retrieve, and process coding preferences.

## Prerequisites

-   mem0-mcp server running and accessible
-   n8n instance installed and running
-   Basic understanding of n8n workflows

## Setup

### 1. Install n8n

If you don't have n8n installed yet, you can install it using npm:

```bash
npm install n8n -g
```

Or run it with Docker:

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### 2. Create HTTP Request Nodes

The mem0-mcp server exposes a REST API at the `/mcp` endpoint. You can use n8n's HTTP Request node to interact with this API.

#### Add Coding Preference

1. Add an HTTP Request node
2. Configure it as follows:
    - **Method**: POST
    - **URL**: `http://your-server:8080/mcp`
    - **Headers**: Content-Type: application/json
    - **Body**:
        ```json
        {
            "name": "add_coding_preference",
            "arguments": {
                "title": "My Code Snippet",
                "content": "console.log('Hello World');",
                "language": "javascript",
                "description": "Simple hello world example",
                "tags": ["javascript", "beginner"]
            }
        }
        ```

#### Get All Coding Preferences

1. Add an HTTP Request node
2. Configure it as follows:
    - **Method**: POST
    - **URL**: `http://your-server:8080/mcp`
    - **Headers**: Content-Type: application/json
    - **Body**:
        ```json
        {
            "name": "get_all_coding_preferences",
            "arguments": {}
        }
        ```

#### Search Coding Preferences

1. Add an HTTP Request node
2. Configure it as follows:
    - **Method**: POST
    - **URL**: `http://your-server:8080/mcp`
    - **Headers**: Content-Type: application/json
    - **Body**:
        ```json
        {
            "name": "search_coding_preferences",
            "arguments": {
                "query": "javascript function"
            }
        }
        ```

### 3. Process the Response

Use n8n's JSON node to parse and process the response from the mem0-mcp server:

1. Add a JSON node after your HTTP Request node
2. Connect the output of the HTTP Request node to the JSON node
3. Configure the JSON node to extract specific fields from the response

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

## Environment Variables

To make your workflows more flexible, use environment variables in n8n:

1. Go to Settings > Variables
2. Add variables like:
    - `MEM0_MCP_URL`: URL of your mem0-mcp server
    - `MEM0_API_KEY`: Your mem0 API key

Then use these variables in your workflows:

```
{{$env.MEM0_MCP_URL}}/mcp
```

## Troubleshooting

-   **Connection issues**: Ensure your mem0-mcp server is accessible from n8n
-   **Authentication errors**: Verify your mem0 API key is correct
-   **404 errors**: Check the server endpoint URL is correct
-   **Parsing errors**: Ensure your JSON payloads are correctly formatted

## Advanced Integration

For more advanced integrations, you can:

1. Create custom n8n nodes that directly interface with mem0-mcp
2. Set up webhooks to trigger workflows when new coding preferences are added
3. Use n8n's error handling features to retry failed requests

## Resources

-   [n8n Documentation](https://docs.n8n.io/)
-   [HTTP Request Node Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
-   [JSON Node Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.json/)
