# The Schedule class represents the complete schedule of datetime-marked events of a user.

from flask_backend.modules.daily_timetable import DailyTimetable
from datetime import date
from typing import List

class Schedule:
    def __init__(self, days_list: List[DailyTimetable]):
        self.days_list = days_list

    # Getter for size of the schedule
    def size(self):
        return len(self.days_list)
    
    # Getter for individual days of the schedule by the date, and returns a DailyTimetable object
    def get_day_by_date(self, target_date: date) -> DailyTimetable:
        for day in self.days_list: 
            if day.get_events() and day.get_events()[0].start.date() == target_date:
                return day
        return DailyTimetable([])  # return empty timetable if no events




