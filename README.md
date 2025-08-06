# Agent Authorization Without the Pain

Your agent needs to access Google Calendar and Gmail. Simple, right? Until you realize you need OAuth flows, token refresh logic, and secure credential storage. Multiply that by every API your agent needs.

This project shows how to connect agents to 250+ APIs using [Composio](https://composio.dev/) and [Model Context Protocol](https://modelcontextprotocol.io/) (MCP). Composio handles authorization and tool execution, so your agents focus on reasoning, not plumbing.

More details in this [blog post](docs/blog-post.md).

## Setup

### Environment

```bash
uv sync
```

### API keys

Make sure you have an account at [Composio](https://composio.dev/). Get an API key from the [developer dashboard](https://app.composio.dev/developer) and set the `COMPOSIO_API_KEY` in `.env`. The [example](#example) uses a [Pydantic AI](https://ai.pydantic.dev/) agent backed by `openai:o4-mini` which requires an `OPENAI_API_KEY`.

```env
COMPOSIO_API_KEY=...
OPENAI_API_KEY=...
```

## Example

Setup MCP servers for Gmail and Google Calendar at Composio. The following script will also open 2 browser tabs with the OAuth consent screens for authorizing access to Gmail and Google Calendar.

```bash
uv run python examples/setup_mcp_composio.py
```

Have a conversation with an agent that uses the Gmail and Google Calendar MCP servers.

```bash
uv run python examples/use_mcp_server_pydantic_ai.py
```
