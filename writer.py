from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from config import Config
from file_ops import save_report_tool

# Writer gets the File Tool
llm = ChatGroq(
    temperature=0, 
    model_name=Config.MODEL_NAME,
    api_key=Config.GROQ_API_KEY
)

writer_tools = [save_report_tool]
llm_writer = llm.bind_tools(writer_tools)

def writer_node(state):
    """
    The Writer Agent Node.
    It analyzes the conversation history (research findings) 
    and writes the final report using the save_report_tool.
    """
    # Force the agent to know its goal
    messages = state["messages"]
    
    # We inject a steering prompt to ensure it calls the tool
    steering_message = SystemMessage(
        content="You are a Technical Writer. Summarize the research above into a professional, "
                "detailed, and comprehensive report. \n\n"
                "Structure the report with the following clearly defined sections using Markdown headers:\n"
                "# Executive Summary\n"
                "# Key Findings\n"
                "# Detailed Analysis\n"
                "# Implications\n"
                "# Future Outlook\n\n"
                "Use bullet points, bold text for emphasis, and clear paragraphs. "
                "Ensure the content is rich, insightful, and not scanty. "
                "THEN, you MUST use the 'save_report_tool' to save it as a .docx file."

    )
    
    response = llm_writer.invoke(messages + [steering_message])
    return {"messages": [response]}
