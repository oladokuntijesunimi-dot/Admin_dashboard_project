import numexpr
from langchain_core.tools import tool

@tool
def calculator_tool(expression: str):
    """
    Evaluates a mathematical expression (e.g., '200 * 1.5').
    Use this when you need to crunch numbers found in research.
    """
    try:
        return str(numexpr.evaluate(expression))
    except Exception as e:
        return f"Error calculating: {e}"
