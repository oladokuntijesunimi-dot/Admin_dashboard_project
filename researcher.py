from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from config import Config
from search import get_search_tool
from calculator import calculator_tool

# Initialize Groq LLM
llm = ChatGroq(
    temperature=0.1, 
    model_name=Config.MODEL_NAME,
    api_key=Config.GROQ_API_KEY
)

# Bind tools (Search & Calc)
research_tools = [get_search_tool(), calculator_tool]
llm_with_tools = llm.bind_tools(research_tools)

def researcher_node(state):
    """
    The Research Agent Node.
    It looks at the state and decides to search, calculate, or stop.
    """
    return {"messages": [llm_with_tools.invoke(state["messages"])]}
