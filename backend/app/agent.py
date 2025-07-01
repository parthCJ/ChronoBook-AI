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
api_key = os.getenv("API_KEY")
print(api_key)

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature="0.3",
    api_key = api_key
)



tools = [check_availability_tool, book_appointment_tool]
functions = [convert_to_openai_function(t) for t in tools]
model = model.bind(functions=functions)

