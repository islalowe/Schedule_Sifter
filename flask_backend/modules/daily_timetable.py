# The DailyTimetable class represents the daily schedule of datetime-marked events of a user.

from flask_backend.modules.event import Event
from typing import List


class DailyTimetable:
    def __init__(self, events_list: List[Event]):
        self.events_list = events_list

    # Getter for the events list of the day
    def get_events(self):
        return self.events_list
    
    # Getter for a specific event
    def get_event(self, index):
        return self.events_list[index]
