# The TimeSlot class is a lightweight object, used for returning vallues from the schedule comparison to the user. 

from datetime import datetime, time, date

class TimeInterval:
    def __init__(self, start: datetime, end: datetime):
        # if start.tzinfo is None or end.tzinfo is None:
        #     raise ValueError("TimeInterval requires timezone-aware datetimes")
        self.start = start
        self.end = end