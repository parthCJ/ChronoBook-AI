from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'parthsharmacj@gmail.com'

def get_calendar_service(credentials_path='service-accoint.json'):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES)
    return build('calendar', 'v3', credentials=credentials)

def check_availability(date, duration_minutes=60):
    service = get_calendar_service()
    start_time = datetime.datetime.strptime(date, '%Y-%m-%d').replace(hour=0, minute=0).isoformat() + 'Z'
    end_time = (datetime.datetime.strptime(date, '%Y-%m-%d') + 
                datetime.timedelta(days=1)).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # Generate all possible time slots (9AM-5PM)
    start_hour = 9
    end_hour = 17
    time_slots = []
    current_time = datetime.datetime.strptime(date, '%Y-%m-%d').replace(hour=start_hour, minute=0)
    
    while current_time.hour < end_hour:
        time_slots.append(current_time.strftime('%H:%M'))
        current_time += datetime.timedelta(minutes=30)
    
    # Remove busy slots
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if 'T' in start:
            event_time = datetime.datetime.fromisoformat(start).strftime('%H:%M')
            if event_time in time_slots:
                time_slots.remove(event_time)
    
    return time_slots

def create_event(summary, date, time):
    service = get_calendar_service()
    start_time = f"{date}T{time}:00+00:00"
    end_time = (datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M") + 
               datetime.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': end_time, 'timeZone': 'UTC'},
    }
    
    created_event = service.events().insert(
        calendarId=CALENDAR_ID,
        body=event
    ).execute()
    
    return f"Booked: {summary} on {date} at {time} (Event ID: {created_event['id']})"