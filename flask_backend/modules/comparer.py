# The Comparer class contains the schedule comparison functionality

from datetime import datetime, time, date, timedelta
from zoneinfo import ZoneInfo
from typing import List
from flask_backend.modules.schedule import Schedule
from flask_backend.modules.time_interval import TimeInterval


class Comparer:
    def __init__(self):
        pass


    # This method compares two given schedules and returns a list of common free TimeInterval objects.
    # todo should the schedules be sorted? would the events ever get out of order?
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
        TODAY = date.today()
        # This is the final product of the search, it is returned to the user.
        common_free_time: List[TimeInterval] = []     # clear the list
        num_search_days = min(s1.size(), s2.size(), days_to_check)
        print(f"Number of days to search: {num_search_days}")
        for curr_day in range(num_search_days):
            print(f"Now comparing day #{curr_day + 1}")
            target_date = date.today() + timedelta(days=curr_day)       # A datetime.date object
            # This holds one-day-only comparison results
            day_common_free_time: List[TimeInterval] = []
            day_common_free_time = self.compare_two_for_one_day(s1.get_day(curr_day), s2.get_day(curr_day), min_hours, target_date)
            # Add the time intervals returned by the one-day comparison to the total comparison result 
            common_free_time.extend(day_common_free_time)
        # Return the result of the schedule comparison
        return common_free_time    


    #todo update eod, hour, and prev_interval_end_time
    def compare_two_for_one_day(self, s1_day, s2_day, min_hours: int, target_date):
        # Instantiate a TimeInterval with start and end times at 00
        free_time_interval = TimeInterval(time(0, 0), time(0, 0), target_date)
        # Instantiate the curr_hour at midnight to begin the comparison
        curr_hour = datetime.combine(target_date, time(00, 00))
        END_OF_DAY = datetime.combine(target_date, time(23, 59))
        prev_interval_end_time = time(0,0)

        # This holds one-day-only comparison results 
        day_common_free_time: List[TimeInterval] = []

        s1_curr_event_tracker = 0
        s2_curr_event_tracker = 0
        # Look through the schedule for each day. curr_day is List object from a DailyTimetable instance
        s1_curr_day = s1_day
        s2_curr_day = s2_day
        # Grab the current event (the first one). curr_event is an event object and an index in the DaityTiimetable
        s1_curr_event = s1_curr_day[s1_curr_event_tracker]
        s2_curr_event = s2_curr_day[s2_curr_event_tracker]


        while curr_hour < END_OF_DAY:
            # todo check to see what happens if events start and end on the same hour mark
            # Accruing free time, and when an event starts, free time ends.
            # if (s1.curr_event.starts now or s2.curr_event starts now):
            if (s1_curr_event.start == curr_hour or s2_curr_event.start == curr_hour):
                # update curr event tracker
                if (s1_curr_event.start == curr_hour):
                    s1_curr_event_tracker += 1
                    s1_curr_event = s1_curr_day[s1_curr_event_tracker]
                else: 
                    s2_curr_event_tracker += 1
                # Make sure the time interval passes the minimum hours threshold
                if (self.check_min_hours(free_time_interval, min_hours)):
                    # Send the completed interval
                    day_common_free_time.append(free_time_interval)

                # Now, we are in the middle of an event. Time passes until *both* schedules have no running events.
                # This loop ends once both schedule's current events end.
                end_time = max(s1_curr_event.end, s2_curr_event.end)

                while curr_hour < end_time:    # Hour increases as time passes until the last event ends
                    curr_hour = self.add_hour(curr_hour)

                # Now, the event ended for both. Free time may resume.
                prev_interval_end_time = curr_hour
                new_interval_start_time = curr_hour
                
            # If an event has not started this hour, The free time interval does not end
            # so we increment the end of the free time interval by 1 hour
            else:
                #todo problem - move to helper function later
                free_time_interval_end_as_datetime = datetime.combine(target_date, free_time_interval.end)
                free_time_interval_endtime = free_time_interval_end_as_datetime + timedelta(hours=1)
                free_time_interval.end = free_time_interval_endtime.time()
            curr_hour = self.add_hour(curr_hour)   # Either way, an hour passes. 
            print("we know an event has started")
        return day_common_free_time


    # Helper method to be able to compare time of events to hour increments in a 24 hour day.
    def convert_to_date_time(self, d: date, t: time) -> datetime:
        return datetime.combine(d, t)
    

    # Helper method to be check whether a time interval passses the minimum length to be added to results.
    def check_min_hours(self, free_time_interval, min_hours):
        dt_start = datetime.combine(free_time_interval.date, free_time_interval.start)
        dt_end = datetime.combine(free_time_interval.date, free_time_interval.end)
        duration = dt_end - dt_start
        if duration >= timedelta(hours=min_hours):
            return True
        return False
    

    # Helper method to add an hour to the datetime object
    # datetime.time does not support arithmetic with timedelta. Only datetime.datetime and datetime.date do.
    def add_hour(self, dt: datetime):
        return dt + timedelta(hours=1)














