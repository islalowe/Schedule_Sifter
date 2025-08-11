# This file is a main interaction point with the rest of the code, simlating a user's interaction with an API

from flask_backend.modules.event import Event
from flask_backend.modules.schedule import Schedule
from flask_backend.modules.daily_timetable import DailyTimetable
from flask_backend.modules.comparer import Comparer
from datetime import datetime, time, timedelta


# today = datetime.today().date()

event1 = Event("Meeting",123,
    datetime.combine(datetime(2025, 8, 17).date(), time(9, 0)),
    datetime.combine(datetime(2025, 8, 17).date(), time(10, 0)))
event2 = Event("Class", 234, 
    datetime.combine(datetime(2025, 8, 17).date(), time(11, 0)), 
    datetime.combine(datetime(2025, 8, 17).date(), time(15, 0)))
event3 = Event("Class", 345, 
    datetime.combine(datetime(2025, 8, 17).date(), time(17, 0)), 
    datetime.combine(datetime(2025, 8, 17).date(), time(23, 0)))

event4 = Event("Class", 987, 
    datetime.combine(datetime(2025, 8, 17).date(), time(7, 0)), 
    datetime.combine(datetime(2025, 8, 17).date(), time(10, 0)))
event5 = Event("Class", 876, 
    datetime.combine(datetime(2025, 8, 17).date(), time(11, 0)), 
    datetime.combine(datetime(2025, 8, 17).date(), time(15, 0)))
event6 = Event("Class", 765, 
    datetime.combine(datetime(2025, 8, 17).date(), time(18, 0)), 
    datetime.combine(datetime(2025, 8, 17).date(), time(22, 0)))

event7 = Event("Class", 456, 
    datetime.combine(datetime(2025, 8, 18).date(), time(10, 0)), 
    datetime.combine(datetime(2025, 8, 18).date(), time(15, 0)))
event8 = Event("Class", 567, 
    datetime.combine(datetime(2025, 8, 18).date(), time(19, 0)), 
    datetime.combine(datetime(2025, 8, 18).date(), time(20, 0)))

event9 = Event("Class", 654, 
    datetime.combine(datetime(2025, 8, 18).date(), time(11, 0)), 
    datetime.combine(datetime(2025, 8, 18).date(), time(15, 0)))
event10 = Event("Class", 543, 
    datetime.combine(datetime(2025, 8, 18).date(), time(18, 0)), 
    datetime.combine(datetime(2025, 8, 18).date(), time(19, 0)))

event11 = Event("Class", 654, 
    datetime.combine(datetime(2025, 8, 19).date(), time(10, 0)), 
    datetime.combine(datetime(2025, 8, 19).date(), time(12, 0)))
event12 = Event("Class", 543, 
    datetime.combine(datetime(2025, 8, 19).date(), time(18, 0)), 
    datetime.combine(datetime(2025, 8, 19).date(), time(22, 0)))

event13 = Event("Class", 654, 
    datetime.combine(datetime(2025, 8, 19).date(), time(8, 0)), 
    datetime.combine(datetime(2025, 8, 19).date(), time(9, 0)))
event14 = Event("Class", 543, 
    datetime.combine(datetime(2025, 8, 19).date(), time(20, 0)), 
    datetime.combine(datetime(2025, 8, 19).date(), time(21, 0)))


# Some Days
# Wrap each day's events in a DailyTimetable object
day_17aug_v1 = DailyTimetable([event1, event2, event3])
day_17aug_v2 = DailyTimetable([event4, event5, event6])
day_18aug_v1 = DailyTimetable([event7, event8])
day_18aug_v2 = DailyTimetable([event9, event10])
day_19aug_v1 = DailyTimetable([event11, event12])
day_19aug_v2 = DailyTimetable([event13, event14])


# Two schedules
s1 = Schedule([day_17aug_v1, day_18aug_v1, day_19aug_v1])
s2 = Schedule([day_17aug_v2, day_18aug_v2, day_19aug_v2])

# checking schedule contents
print("Schedule 1:")
for day in s1.days_list:
    print(day.get_events())

print("\nSchedule 2:")
for day in s2.days_list:
    print(day.get_events())


# Instantiate comparer and compare
comparer = Comparer()
common_free = comparer.compare_two_schedules(s1, s2, 4, 1)
if common_free:
    print(f"Found {len(common_free)} common intervals.")
    # Show results
    print("Here are the final results of the comparison:")
    for interval in common_free:
       print(f"{interval.start.date()} — {interval.start.time()} to {interval.end.time()}")

else:
    print("No common intervals were found (or compare_two_schedules returned None).")


