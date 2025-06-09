# The DailyTimetable class represents the daily schedule of datetime-marked events of a user.

from event import Event
from typing import List

class DailyTimetable:
    def __init__(self, events_list: List[Event]):
        self.events_list = events_list

    # Getter for size of the schedule
    def size(self):
        return len(self.days_list)