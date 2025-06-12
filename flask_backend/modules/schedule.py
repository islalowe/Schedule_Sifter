# The Schedule class represents the complete schedule of datetime-marked events of a user.

from flask_backend.modules.daily_timetable import DailyTimetable
from typing import List

class Schedule:
    def __init__(self, days_list: List[DailyTimetable]):
        self.days_list = days_list

    # Getter for size of the schedule
    def size(self):
        return len(self.days_list)
    
    # Getter for days
    def get_day(self, index):
        return self.days_list[index]



