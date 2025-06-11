import asyncio
import nest_asyncio
from langchain_groq import ChatGroq
 
from mcp_use import MCPAgent, MCPClient
from mcp import ClientSession
from mcp.client.sse import sse_client
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

nest_asyncio.apply()

#Steps:
#1 Sever is running before running the script
#2 Server is configured using SSE transport
#3 Server is listening on port 8000

async def main():
    async with sse_client(url="https://localhost:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream=read_stream, write_stream=write_stream) as session:
            await session.initialize()
    
            tools_result = await session.list_tools()
            print("Available tools")
            for tool in tools_result.tools:
                print(f" - {tool.name}: {tool.description}")
            
            result = await session.call_tool("get_slerts", arguments={"state":"CA"})
            print(f"The weather alerts are = {result.content[0].text}")
if __name__=="__main__":
    asyncio.run(main())