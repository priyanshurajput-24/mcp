"""
    This file is the real demonstration of MCP client.
    Here we can see how LLM is using the context for differnt type of tasks.
    We can see how it is evaluating the math expression and fromattig the Weather API response.

"""


from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from typing import Dict, Any
import asyncio

from dotenv import load_dotenv
load_dotenv()


async def get_weather_context(state: str, client: MultiServerMCPClient) -> Dict[str, Any]:
    """Get weather context for a specific state."""
    tools = await client.get_tools()
    weather_tool = next((tool for tool in tools if tool.name == "get_alerts"), None)
    
    if weather_tool:
        response = await weather_tool.ainvoke({"state": state})
        return {
            "state": state,
            "alerts": response,
            "timestamp": asyncio.get_event_loop().time()
        }
    return {"error": "Weather tool not found"}



async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    import os
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()
    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model, tools)
    colored_sep = "\033[31m*************************************************\033[0m"  # Red color


    # Get weather context for California
    weather_context = await get_weather_context("CO", client)
    
    # Pass the context in the message with explicit state reference
    weather_response = await agent.ainvoke({
        "messages": [{
            "role": "user", 
            "content": f"Here are the weather alerts for {weather_context['state']}. Please analyze and summarize data in 3 sentences: {weather_context['alerts']}"
        }]
    })
    
    print(f"{colored_sep}")
    print("Weather response with context:", weather_response['messages'][-1].content)


    print(f"{colored_sep}")
    print(f"{colored_sep}\n")


    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's [(3 + 5) x (12-3+4) + 10] * 2 ?"}]}
    )

    print("Math response:", math_response['messages'][-1].content)



if __name__ == "__main__":
    asyncio.run(main())
