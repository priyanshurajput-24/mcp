"""
    This file is the real demonstration of MCP client.
    Here we can see how LLM is using the context for differnt type of tasks.
    We can see how resources and prompts are used to provide context-aware responses.

"""


from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from typing import Dict, Any
from langchain_mcp_adapters.resources import load_mcp_resources
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()


async def get_csv_context(file_path: str, client: MultiServerMCPClient) -> Dict[str, Any]:
    """Get CSV data context for a specific file."""
    tools = await client.get_tools()
    csv_tool = next((tool for tool in tools if tool.name == "process_csv"), None)
    
    if csv_tool:
        response = await csv_tool.ainvoke({"file_path": file_path})
        return {
            "file_path": file_path,
            "data": response,
            "timestamp": asyncio.get_event_loop().time()
        }
    return {"error": "CSV processing tool not found"}



async def main():

    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "csv_processor": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    
    # Static resources loading
    resources = await client.get_resources(server_name="math")
    for blob in resources:
        print(blob.as_string())  # or blob.as_bytes() for binary data

    math_resources = blob.as_string()

    # Dynamic resources loading
    resources = await client.get_resources(server_name="math", uris="greetings://Alice")
    for blob in resources:
        print(blob.as_string())  # or blob.as_bytes() for binary data



    
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()
    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model, tools)
    colored_sep = "\033[31m*************************************************\033[0m"  # Red color



    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": f"This is math context: {math_resources}. what's [(3 + 5) x (12-3+4) + 10] * 2 ?  Please provide the author name ?"}]}
    )

    print("Math response:", math_response['messages'][-1].content)


    # Example CSV file path - replace with your actual CSV file path
    csv_file_path = os.getenv("CSV_FILE_PATH")  # Ensure this file exists in your environment
    
    # Get CSV context
    csv_context = await get_csv_context(csv_file_path, client)
    
    # Pass the context to the agent for analysis
    csv_response = await agent.ainvoke({
        "messages": [{
            "role": "user", 
            "content": f"Here is the CSV data from {csv_context['file_path']}. Please analyze the data and provide insights about the dataset structure and potential patterns: {csv_context['data']}"
        }]
    })
    
    print(f"{colored_sep}")
    print("CSV Analysis Response:", csv_response['messages'][-1].content)


    # Prompt template demo
    prompt_resources = await client.get_prompt(prompt_name="ask_about_topic",server_name="math",arguments={"topic": "machine learning"})
    for msg in prompt_resources:
        print(msg.content)

    # prompt with different functon URI
    prompt_resources = await client.get_prompt(prompt_name="ask_about_topic_2",server_name="math",arguments={"topic": "machine learning"})
    for msg in prompt_resources:
        print(msg.content)


    # Prompt with multiple arguments    
    prompt_resources = await client.get_prompt(prompt_name ="generate_code_request",server_name="math",arguments={"language": "python", "task_description": "calculate the square root of a number"})
    for msg in prompt_resources:
        print(msg.content)

    # Using the prompt-generated message
    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": msg.content}]
    })
    print("LLM response to prompt-generated message:", response['messages'][-1].content)



if __name__ == "__main__":
    asyncio.run(main())


