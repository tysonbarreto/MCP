import asyncio
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from mcp_use import MCPClient, MCPAgent

import os, sys, time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

async def run_memory_chat():
    """
    Run a chat using MCPAgent's built-in conversation memory.
    """
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    client = MCPClient.from_config_file(filepath="weather.json")
    llm = ChatGroq(model="qwen-qwq-32b")

    agent = MCPAgent(
        llm = llm,
        client=client,
        max_steps=5,
        memory_enabled=True
    )

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")
    try:
        # Main chat loop
        while True:
            # Get user input
            user_input = input("\nYou: ")

            match user_input.lower():
                case ["exit", "quit"]:
                    print("Ending conversation...")
                    await client.close_all_sessions()

                case "clear":
                    agent.clear_conversation_history()
                    print("Conversation history cleared.")
                    continue

            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                for line_ in response:
                    time.sleep(0.075)
                    sys.stdout.write(line_)
                    sys.stdout.flush()

            except Exception as e:
                print(f"\nError: {e}")
    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
            