"""
    This the MCP server for math operations.
"""

from mcp.server.fastmcp import FastMCP
from fastmcp.prompts.base import UserMessage, TextContent


mcp=FastMCP("Math")

@mcp.tool()
def add(a:int,b:int)->int:
    """_summary_
    Add to numbers
    """
    return a+b

@mcp.tool()
def multiple(a:int,b:int)-> int:
    """Multiply two numbers"""
    return a*b


# 3. for two static resource change the name of resource to config1 and config2
@mcp.resource("resource://config1")
def get_config1() -> dict:
    """Provides the application's configuration."""
    return {"version": "1.0", "author": "MyTeam"}

# 3. static resource
@mcp.resource("resource://config2")
def get_config2() -> dict:
    """Provides the application's configuration."""
    return {"version": "2.0", "author": "MyTeam_11"}




# 4. Add a resource template for dynamic content
@mcp.resource("greetings://{name}")
def personalized_greeting(name: str) -> str:
    """Generates a personalized greeting for the given name."""
    return f"Hello, {name}! Welcome to the MCP server."



# Basic prompt returning a string (converted to user message automatically)
@mcp.prompt()
def ask_about_topic(topic: str) -> str:
    """Generates a user message asking for an explanation of a topic."""
    return f"Can you please explain the concept of '{topic}'?"


# Basic prompt returning a string (converted to user message automatically)
@mcp.prompt()
def ask_about_topic_2(topic: str) -> str:
    """Generates a user message asking for an explanation of a topic."""
    return f"Can you please explain the concept of _ 22 '{topic}'?"




# Prompt returning a specific message type
@mcp.prompt()
def generate_code_request(language: str, task_description: str) -> UserMessage:
    """Generates a user message requesting code generation."""
    content = f"Write a {language} function that performs the following task: {task_description}"
    return UserMessage(role="user", content=TextContent(type="text", text=content))




if __name__=="__main__":
    mcp.run(transport="stdio")
