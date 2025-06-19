"""
    This is the MCP server for processing CSV files and passing data to a model.
    It handles CSV file reading and data processing.
"""

import pandas as pd
from mcp.server.fastmcp import FastMCP
from typing import Any, List, Dict
import os


mcp = FastMCP("csv_processor")

async def read_csv_file(file_path: str) -> pd.DataFrame | None:
    """Read a CSV file and return its contents as a DataFrame."""
    try:
        if not os.path.exists(file_path):
            return None
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return None

def format_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Format DataFrame into a list of dictionaries for model processing."""
    return df.to_dict('records')

@mcp.tool()
async def process_csv(file_path: str) -> str:
    """Process a CSV file and prepare its data for model input.

    Args:
        file_path: Path to the CSV file to process
    """
    df = await read_csv_file(file_path)
    
    if df is None:
        return "Unable to read CSV file. Please check if the file exists and is properly formatted."
    
    if df.empty:
        return "The CSV file is empty."
    
    # Format the data for model processing
    formatted_data = format_data(df)
    
    # Here you would typically pass the data to your model
    # For now, we'll just return a summary of the data
    return f"""
    Successfully processed CSV file:
    - Number of rows: {len(df)}
    - Number of columns: {len(df.columns)}
    - Columns: {', '.join(df.columns)}
    """

if __name__ == "__main__":
    mcp.run(transport="streamable-http") 