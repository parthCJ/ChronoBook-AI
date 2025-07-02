# from langchain_community.chat_models import ChatDeepSeek
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatMessagePromptTemplate, MessagesPlaceholder
from langgraph.graph import END, MessageGraph
from tools import CheckAvailabilityInput, BookAppointmentInput, check_availability_tool, book_appointment_tool, parse_date
from langchain.tools.render import format_tool_to_openai_function
import json
from dotenv import load_dotenv
import os
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
print(api_key)

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature="0.3",
    api_key = api_key
)



tools = [check_availability_tool, book_appointment_tool]
functions = [convert_to_openai_function(t) for t in tools]
model = model.bind(functions=functions)


# Create the agent workflow
def should_use_tool(state):
    last_message = state[-1]
    if "book" in last_message.content.lower() or "appointment" in last_message.content.lower():
        return "use_tool"
    return "generate_response"

# Create the agent workflow
def should_use_tool(state):
    """
    Determines whether to use a tool based on the content of the last message.

    Args:
        state (List[Message]): The conversation history, where each item has a 'content' attribute.

    Returns:
        str: "use_tool" if the last message mentions booking or appointments,
             otherwise "generate_response".
    """
    last_message = state[-1]
    if "book" in last_message.content.lower() or "appointment" in last_message.content.lower():
        return "use_tool"
    
def call_tool(state):
    last_message = state[-1]
    try:
        # Parse tool call from AI message
        tool_call = last_message.additional_kwargs.get("tool_calls", [{}])[0]
        func_name = tool_call['function']['name']
        args = json.loads(tool_call['function']['arguments'])

        if func_name == "check_availability_tool":
            date = parse_date(args.get('date', ''))
            result = check_availability_tool(date)
            return AIMessage(content=f"Available times on {date}: {', '.join(result)}")
        
        elif func_name == "book_appointment_tool":
            date = parse_date(args.get('date', ''))
            result = book_appointment_tool(
                date = date,
                time = args["time"],
                summary=args["summary"]
            )
            return AIMessage(content=result)
        return AIMessage(content="Tool not recognized")
    
    except Exception as e:
        return AIMessage(content=f"Error: {str(e)}")
        

