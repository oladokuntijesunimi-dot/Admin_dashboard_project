from research_flow import app
from langchain_core.messages import HumanMessage

def main():
    print("🚀 Groq Research Agent Starting...")
    
    topic = input("What should I research? (e.g., 'Nvidia Stock Performance 2024'): ")
    
    initial_message = HumanMessage(
        content=f"Research the topic '{topic}'. Use the calculator for any math. "
                "Once you have enough info, pass it to the writer."
    )
    
    print("\nProcessing... (Watch the speed of Groq!)")
    
    # Stream events to show the class what's happening live
    inputs = {"messages": [initial_message]}
    
    for event in app.stream(inputs, stream_mode="values"):
        # Get the latest message
        message = event["messages"][-1]
        
        # Pretty print the output
        if message.content:
            print(f"\n🤖 {message.type.upper()}: {message.content[:100]}...")
        
        if hasattr(message, 'tool_calls') and message.tool_calls:
            print(f"🛠️  CALLING TOOL: {message.tool_calls[0]['name']}")

    print("\n✅ Workflow Finished. Check your folder for the .docx file!")

if __name__ == "__main__":
    main()
