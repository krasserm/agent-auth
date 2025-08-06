import asyncio
import json

import dotenv
from aioconsole import ainput, aprint
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP


async def main():
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
        
    message_history = []    
    
    async with agent:
        while True:
            user_input = await ainput("\n👤 You: ")
            
            if user_input.lower() in ["exit", "quit", "q"]:
                await aprint("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            await aprint("\n🤖 Agent: ", end="", flush=True)

            async with agent.run_stream(user_input, message_history=message_history) as result:
                async for text in result.stream_text(delta=True):
                    await aprint(text, end="", flush=True)
                await aprint()

                message_history.extend(result.new_messages())


if __name__ == "__main__":
    dotenv.load_dotenv()
    asyncio.run(main())
