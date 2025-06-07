# The Schedule class represents the complete schedule of datetime-marked events of a user.

from modules.event import Event
from typing import List

class Schedule:
    def __init__(self, days_list: List[Event]):
        self.days_list = days_list

    # Getter for size of the schedule
    def size(self):
        return len(self.days_list)



# def __init__(self, days_list):
#         self.days_list = days_list