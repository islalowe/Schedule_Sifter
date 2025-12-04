# The Comparer class contains the schedule comparison functionality

from datetime import datetime, time, date, timedelta
from zoneinfo import ZoneInfo
from typing import List
import logging
from flask_backend.modules.schedule import Schedule
from flask_backend.modules.time_interval import TimeInterval

logging.basicConfig(level=logging.ERROR)

class Comparer:
    def __init__(self):
        pass


    # This method compares two given schedules and returns a list of common free TimeInterval objects.
    def compare_two_schedules(self, s1: Schedule, s2: Schedule, days_to_check = 7, min_hours = 1):
        """
        Compare two schedules
        Args:
            s1 (Schedule): First schedule.
            s2 (Schedule): Second schedule.
            days_to_check (int): the number of days in the future to search through
            min_hours (int): the number of hours that will be considered the minimum for a TimeInterval object to be returned

        Returns:
            List: the shared TimeInterval objects.
        """
        #TODAY = date.today()
        # This is the final product of the search, it is returned to the user.
        common_free_time: List[TimeInterval] = []     # clear the list
        num_search_days = min(s1.size(), s2.size(), days_to_check)
        print(f"Number of days to search: {num_search_days}")

        today = datetime.now().date()
        final_day = today + timedelta(days=days_to_check)
        print(f"The schedules will be compared from now until {final_day}")

        curr_date = today
        while curr_date < final_day:
            # Get day's schedules
            s1_day = s1.get_day_by_date(curr_date) 
            s2_day = s2.get_day_by_date(curr_date) 

            print(f"Now comparing {curr_date}")
            if s1_day and s2_day and (s1_day.size() > 0 or s2_day.size() > 0):
                day_common_free_time = self.compare_two_for_one_day(
                    s1_day, s2_day, min_hours, curr_date
                )
                common_free_time.extend(day_common_free_time)
            else: 
                print(f"No events on {curr_date}. Skipping.")

            curr_date += timedelta(days=1)
        return common_free_time
     



    def compare_two_for_one_day(self, s1_day, s2_day, granularity_hours: int, target_date):
        """
        Compare two people's schedules for a specific day and return common free TimeIntervals.
        """
        # This holds one-day-only comparison results 
        day_common_free_time: List[TimeInterval] = []

        # todo This should not be necessary but it's here
        s1_events = sorted(s1_day.get_events(), key=lambda e: e.start)
        s2_events = sorted(s2_day.get_events(), key=lambda e: e.start)

        # Trackers
        s1_index = 0
        s2_index = 0

        curr_hour = datetime.combine(target_date, time(0, 0))
        END_OF_DAY = datetime.combine(target_date, time(23, 59))

        in_free_time = False
        free_interval_start = None

        while curr_hour < END_OF_DAY:
            # Accruing free time, and when an event starts, free time ends.
            someone_busy = False 

            # Check if S1 is busy this hour
            while s1_index < len(s1_events) and s1_events[s1_index].end <= curr_hour:
                s1_index += 1
            if s1_index < len(s1_events) and s1_events[s1_index].start <= curr_hour < s1_events[s1_index].end:
                someone_busy = True

            # Check if S2 is busy this hour
            while s2_index < len(s2_events) and s2_events[s2_index].end <= curr_hour:
                s2_index += 1
            if s2_index < len(s2_events) and s2_events[s2_index].start <= curr_hour < s2_events[s2_index].end:
                someone_busy = True
            
            if not someone_busy:
                if not in_free_time:
                    in_free_time = True
                    free_interval_start = curr_hour
            else:
                if in_free_time:
                # End current free interval
                    free_interval_end = curr_hour
                    interval = TimeInterval(free_interval_start, free_interval_end)
                if self.check_min_hours(interval, granularity_hours):
                    day_common_free_time.append(interval)
                in_free_time = False

            curr_hour = self.add_hour(curr_hour)
         # If we ended the day in a free block, close it
        if in_free_time:
            interval = TimeInterval(free_interval_start, free_interval_end)
        if self.check_min_hours(interval, granularity_hours):
            day_common_free_time.append(interval)

        return day_common_free_time




    # Helper method to be able to compare time of events to hour increments in a 24 hour day.
    def convert_to_date_time(self, d: date, t: time) -> datetime:
        return datetime.combine(d, t)
    

    # Helper method to be check whether a time interval passses the minimum length to be added to results.
    def check_min_hours(self, free_time_interval, min_hours):
        dt_start = free_time_interval.start
        dt_end = free_time_interval.end
        duration = dt_end - dt_start
        if duration >= timedelta(hours=min_hours):
            return True
        return False
    

    # Helper method to add an hour to the datetime object
    # datetime.time does not support arithmetic with timedelta. Only datetime.datetime and datetime.date do.
    def add_hour(self, dt: datetime):
        return dt + timedelta(hours=1)














