# The Person class represents individual users, and maintains their schedules and profiles.

from module.schedule: import Schedule

class Person:
    __init__(self, name: str, schedule: Schedule):
        self.name = name
        self.schedule = schedule
