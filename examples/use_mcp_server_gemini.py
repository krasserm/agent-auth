import asyncio
import json
import os

import dotenv
from google import genai
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

with open("examples/mcp_server_urls.json", "r") as f:
    mcp_urls = json.load(f)
    gcal_mcp_url = mcp_urls["gcal"]

async def main():
    async with streamablehttp_client(gcal_mcp_url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
                        
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents="List my August 2025 calendar events",
                config=genai.types.GenerateContentConfig(
                    tools=[session],
                ),
            )
            print(response.text)
                

if __name__ == "__main__":
    dotenv.load_dotenv()
    asyncio.run(main())
