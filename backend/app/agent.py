# from langchain_community.chat_models import ChatDeepSeek
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatMessagePromptTemplate, MessagesPlaceholder
from langgraph.graph import END, MessageGraph
from tools import CheckAvailabilityInput, BookAppointmentInput, check_availability_tool, book_appointment_tool, parse_date
from langchain.tools.render import format_tool_to_openai_function
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
print(api_key)

# model = ChatDeepSeek(
#     model="deepseek-chat",
#     temperature="0.3",
#     api_key = api_key
# )

