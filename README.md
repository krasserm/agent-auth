## Setup

1. Install dependencies

```bash
uv sync
```

2. API keys

Make sure you have an account at [Composio](https://composio.dev/). Get an API key from the [developer dashboard](https://app.composio.dev/developer) and set the `COMPOSIO_API_KEY` in `.env`. 
The agent examples use use Google `gemini-2.5-flash` and OpenAI `o4-mini` as models which need a `GEMINI_API_KEY` and `OPENAI_API_KEY`, respectively.

```env
COMPOSIO_API_KEY=...
GEMINI_API_KEY=...
OPENAI_API_KEY=...
```

## Examples

1. Setup MCP servers for Gmail and Google Calendar at Composio. This will open 2 browser tabs with the OAuth consent screens for authorizing access to Gmail and Google Calendar.

```bash
python examples/setup_mcp_composio.py
```

2. Run the agent examples

```bash
python examples/use_mcp_server_pydantic_ai.py
python examples/use_mcp_server_gemini.py
```
