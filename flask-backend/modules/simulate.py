# This file is a main interaction point with the rest of the code, simlating a user's interaction with an API

from modules.event import Event
from modules.schedule import Schedule
from modules.comparer import Comparer
from datetime import datetime, time, timedelta


# today = datetime.today().date()

event1 = Event("Meeting",123,
    datetime.combine(datetime(2025, 6, 7).date(), time(9, 0)),
    datetime.combine(datetime(2025, 6, 7).date(), time(10, 0)))
event2 = Event("Class", 234, 
    datetime.combine(datetime(2025, 6, 7).date(), time(11, 0)), 
    datetime.combine(datetime(2025, 6, 7).date(), time(15, 0)))
event3 = Event("Class", 345, 
    datetime.combine(datetime(2025, 6, 7).date(), time(17, 0)), 
    datetime.combine(datetime(2025, 6, 7).date(), time(23, 0)))
event4 = Event("Class", 456, 
    datetime.combine(datetime(2025, 6, 8).date(), time(10, 0)), 
    datetime.combine(datetime(2025, 6, 8).date(), time(15, 0)))
event5 = Event("Class", 567, 
    datetime.combine(datetime(2025, 6, 8).date(), time(19, 0)), 
    datetime.combine(datetime(2025, 6, 8).date(), time(20, 0)))

event6 = Event("Class", 987, 
    datetime.combine(datetime(2025, 6, 7).date(), time(7, 0)), 
    datetime.combine(datetime(2025, 6, 7).date(), time(10, 0)))
event7 = Event("Class", 876, 
    datetime.combine(datetime(2025, 6, 7).date(), time(11, 0)), 
    datetime.combine(datetime(2025, 6, 7).date(), time(15, 0)))
event8 = Event("Class", 765, 
    datetime.combine(datetime(2025, 6, 7).date(), time(18, 0)), 
    datetime.combine(datetime(2025, 6, 7).date(), time(22, 0)))
event9 = Event("Class", 654, 
    datetime.combine(datetime(2025, 6, 8).date(), time(11, 0)), 
    datetime.combine(datetime(2025, 6, 8).date(), time(15, 0)))
event10 = Event("Class", 543, 
    datetime.combine(datetime(2025, 6, 8).date(), time(18, 0)), 
    datetime.combine(datetime(2025, 6, 8).date(), time(19, 0)))



# Two schedules
s1 = Schedule([event1, event2, event3, event4, event5])
s2 = Schedule([event6, event7, event8, event9, event10])

# Instantiate comparer and compare
comparer = Comparer()
common_free = comparer.CompareTwoSchedules(s1, s2, 3, 1)

# Show results
for interval in common_free:
    print(f"{interval.date} — {interval.start} to {interval.end}")
