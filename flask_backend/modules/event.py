# The Event class represents individual calendar events

from datetime import datetime

class Event:
    def __init__(self, eventId: int, start: datetime, end: datetime, name: str = "no name"):
        self.eventId = eventId
        self.name = name
        self.start = start
        self.end = end

        
        # Getter for the event
        def get_event(self):
            return self

        # Getter for start of the event
        #todo maybe the is unecessary?
        def get_event_start(self):
            return self.start
        
        # Getter for end of the event
            return self.end


