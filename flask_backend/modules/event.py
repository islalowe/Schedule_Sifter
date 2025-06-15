# The Event class represents individual calendar events

from datetime import datetime

class Event:
    def __init__(self, name: str, eventId: int, start: datetime, end: datetime):
        self.eventId = eventId
        self.name = name
        self.start = start
        self.end = end

        
    # Getter for the event
    def get_event(self):
        return self
        
    # Getter for a date
    def get_event_date(self):
        return self.start.date()

    def __repr__(self):
        return f"Event({self.name}, {self.start}, {self.end})"
        



