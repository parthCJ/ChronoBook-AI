from pydantic import BaseModel, Field
from calender import check_availability
from calender import create_event
from datetime import datetime, timedelta
import lance
import re
from langchain.tools import tool 
class CheckAvailabilityInput(BaseModel):
    date: str = Field(description="Date in YYYY-MM-DD format to check availability")
    
class BookAppointmentInput(BaseModel):
    date: str = Field(description="Date in YYYY-MM-DD format")
    time: str = Field(description="Time in HH:MM format")
    summary: str = Field(description="Appointment summary")

@tool
def check_availability_tool(date: str):
    """check availability for the appointment"""
    return check_availability(date)
@tool
def book_appointment_tool(date: str, time: str, summary: str):
    """book the appointment"""
    return create_event(date)

def parse_date(text: str) -> str:
    today = datetime().date()

    if "today" in text.lower():
        return today.strftime('%Y-%m-%d')
        
    if "tomorrow" in text.lower():
        return (today + timedelta(days=1)).strftime('%Y-%m-%d')
    
    day_match = re.search(r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', text, re.I)
    if day_match:
        day_name = day_match.group(0).lower()
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        target_idx = days.index(day_name)
        current_idx = today.weekday()
        days_ahead = (target_idx - current_idx) % 7
        if days_ahead == 0: days_ahead = 7
        return (today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
    
    return today.strftime('%Y-%m-%d')