# The Person class represents individual users, and maintains their schedules and profiles.

from flask_backend.modules.schedule import Schedule
from typing import Optional

class User:
     def __init__(self, name: str, schedule: Optional[Schedule] = None):
        self.name = name
        self.schedule = schedule

