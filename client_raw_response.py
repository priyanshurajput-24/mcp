"""
 This is a simple example of how Raw response from LLM looks like.
 For the weather tool API waht's the raw response.

"""


from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from weather import get_alerts
from typing import Dict, Any
import asyncio


from dotenv import load_dotenv
load_dotenv()



async def main():
    client = MultiServerMCPClient()

    import os
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()
    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model, tools)
    colored_sep = "\033[31m*************************************************\033[0m"  # Red color



    print(f"{colored_sep}")
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's [(3 + 5) x (12-3+4) + 10] * 2 ?"}]}
    )
    print("Math response:", math_response['messages'][-1].content)

    print(f"{colored_sep}")
    print(f"{colored_sep}\n")
    weather_context = await get_alerts("CO")
    print("Weather context:", weather_context)



if __name__ == "__main__":
    asyncio.run(main())
