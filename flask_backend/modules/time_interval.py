# The TimeSlot class is a lightweight object, used for returning vallues from the schedule comparison to the user. 

from datetime import datetime, time, date

class TimeInterval:
    def __init__(self, start: time, end: time, date: datetime):
        self.start = start
        self.end = end
        self.date = date