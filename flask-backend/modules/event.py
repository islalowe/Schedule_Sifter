# The Event class represents individual calendar events

from datetime import datetime

class Event:
    def __init__(self, eventId: int, start: datetime, end: datetime, name: str = "no name"):
        self.eventId = eventId
        self.name = name
        self.start = start
        self.end = end


