"""
    This file demonstrates how to use the CSV processor MCP client.
    It shows how the LLM can analyze and provide insights about CSV data using context-aware responses.
"""

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from typing import Dict, Any
import asyncio
import os
from dotenv import load_dotenv
from csv_processor import read_csv_file, format_data

load_dotenv()


# Function that give response without using MCP client or context.
async def main():
    client = MultiServerMCPClient()
    # get csv file path from environment variable
    csv_file_path = os.getenv("CSV_FILE_PATH", "test.csv")
    # read csv file
    df = await read_csv_file(csv_file_path)
    # format data
    formatted_data = format_data(df)
    # pass to model directly
    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model, formatted_data)
    response = await agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": f"Here is the CSV data from {csv_file_path}. Please analyze the data and provide insights about the dataset structure and potential patterns: {formatted_data}"
        }]
    })
    print("CSV Analysis Response:", response['messages'][-1].content)



if __name__ == "__main__":
    asyncio.run(main()) 