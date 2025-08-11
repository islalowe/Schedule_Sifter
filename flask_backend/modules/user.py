# The Person class represents individual users, and maintains their schedules and profiles.

from flask_backend.modules.schedule import Schedule

class User:
    def __init__(self, name: str, schedule: Schedule):
        self.name = name
        self.schedule = schedule
