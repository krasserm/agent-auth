import asyncio
import json
import textwrap
from dataclasses import asdict

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP


async def main():
    # Load MCP URLs from JSON file
    with open("examples/mcp_server_urls.json", "r") as f:
        mcp_urls = json.load(f)
        gcal_mcp_url = mcp_urls["gcal"]
        gmail_mcp_url = mcp_urls["gmail"]

    agent = Agent(
        'openai:o4-mini',
        toolsets=[
            MCPServerStreamableHTTP(gcal_mcp_url),  
            MCPServerStreamableHTTP(gmail_mcp_url),
        ]
    )
    
    prompt = textwrap.dedent("""
        List my Sep 2025 calendar events and save them as draft to my gmail account 
        (subject: Sep 2025 events, recipient: martin@example.com). Show the event
        titles in your response.
    """)

    async with agent:
        result = await agent.run(prompt)
    
    print(result.output)
        
                
if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    asyncio.run(main())
