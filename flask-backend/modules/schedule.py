# The Schedule class represents the complete schedule of datetime-marked events of a user.

from modules.event import Event
from typing import List

class Schedule:
    def __init__(self, daysList: List[Event]):
        self.daysList = daysList