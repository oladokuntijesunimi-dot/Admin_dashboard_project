from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver # Optional: specific for checkpoints
from langgraph.types import RetryPolicy # <--- IMPORT THIS

from researcher import researcher_node, research_tools
from writer import writer_node, writer_tools

# 1. Define State
class AgentState(TypedDict):
    messages: Annotated[List, add_messages]

# 2. Define the Graph
workflow = StateGraph(AgentState)

# --- ERROR HANDLING CONFIG ---
# Retry up to 3 times if there is a network error or API timeout
retry_policy = RetryPolicy(
    max_attempts=3,
    initial_interval=1.0,  # Wait 1s, then 2s, then 4s...
    backoff_factor=2.0,
    retry_on=Exception     # Retry on any crash
)

# 3. Add Nodes with Retry Policy
workflow.add_node("researcher", researcher_node, retry_policy=retry_policy)
workflow.add_node("writer", writer_node, retry_policy=retry_policy)

# --- ROBUST TOOL NODES ---
# handle_tool_errors=True catches crashes and sends "Error: [Details]" to the LLM
# so the LLM can try to fix it instead of the program crashing.

workflow.add_node("research_tools", ToolNode(research_tools, handle_tool_errors=True))
workflow.add_node("writer_tools", ToolNode(writer_tools, handle_tool_errors=True))

# 4. Define Edges (The Logic)
workflow.set_entry_point("researcher")

def researcher_condition(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "research_tools"
    return "writer"

workflow.add_conditional_edges("researcher", researcher_condition)
workflow.add_edge("research_tools", "researcher")

def writer_condition(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "writer_tools"
    return END

workflow.add_conditional_edges("writer", writer_condition)
workflow.add_edge("writer_tools", END)

# 5. Compile
app = workflow.compile()
