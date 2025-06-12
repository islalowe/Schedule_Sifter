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
    def CompareTwoSchedules(self, s1: Schedule, s2: Schedule, days_to_check = 7, min_hours = 1):
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
        # This is the product of the search, it returned to the user.
        common_free_time: List[TimeInterval] = []     # clear the list
        # Find the shortest among s1, s2, and days_to_check
        num_search_days = min(s1.size(), s2.size(), days_to_check)
        # Iterate through the two schedules together
        # Add every consecutive hour that is free for both schedules to a TimeInterval object (may happen multiple times per day)
        for curr_day in range(num_search_days):
            print('comparing a day, using a nested loop')
            # This holds one-day-only comparison results
            day_common_free_time: List[TimeInterval] = []
            day_common_free_time = self.CompareTwoForOneDay(s1.get_day(curr_day), s2.get_day(curr_day), min_hours, curr_day)
            # Add the time intervals returned by the one-day comparison to the total comparison result 
            common_free_time.extend(day_common_free_time)
        # Return the result of the schedule comparison
        return common_free_time    


    #todo update eod, hour, and prev_interval_end_time
    def CompareTwoForOneDay(self, s1_day, s2_day, min_hours: int, check_day: int):
        TODAY = date.today()
        # Instantiate a TimeInterval with start and end times at 00
        #todo make sure day is small to large
        target_date = TODAY + timedelta(days=check_day)
        free_time_interval = TimeInterval(time(0, 0), time(0, 0), target_date)

        curr_hour = datetime.combine(target_date, time(0, 0))
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
            #     if (s1_curr_event.start == curr_hour):
            #         s1_curr_event_tracker += 1
                        #todo increment the event along with the tracker
            #     else: 
            #         s2_curr_event_tracker += 1
            #     # Make sure the time interval passes the minimum hours threshold
            #     if (self.CheckMinHours(free_time_interval, min_hours)):
            #         # Send the completed interval
            #         day_common_free_time.append(free_time_interval)

            #     # Now, we are in the middle of an event. Time passes until *both* schedules have no running events.
            #     # This loop ends once both schedule's current events end.
            #     end_time = max(s1_curr_event.end, s2_curr_event.end)

            #     while curr_hour < end_time:    # Hour increases as time passes until the last event ends
            #         curr_hour = self.AddHour(target_date, hour.time())

            #     # Now, the event ended for both. Free time may resume.
            #     prev_interval_end_time = curr_hour
            #     new_interval_start_time = curr_hour
                
            # # If an event has not started this hour, The free time interval does not end
            # # so we increment the end of the free time interval by 1 hour
            # else:
            #     free_time_interval.end = self.AddHour(target_date, free_time_interval.time())
            # hour = self.AddHour(target_date, curr_hour)   # Either way, an hour passes. 
                print("we know an event has started")
        return day_common_free_time


    # Helper method to be able to compare time of events to hour increments in a 24 hour day.
    def ConvertToDateTime(self, d: date, t: time) -> datetime:
        return datetime.combine(d, t)
    

    # Helper method to be check whether a time interval passses the minimum length to be added to results.
    def CheckMinHours(self, free_time_interval, min_hours):
        dt_start = datetime.combine(free_time_interval.date, free_time_interval.start)
        dt_end = datetime.combine(free_time_interval.date, free_time_interval.end)
        duration = dt_end - dt_start
        if duration >= timedelta(hours=min_hours):
            return True
        return False
    

    # Helper method to add an hour to the datetime object
    # datetime.time does not support arithmetic with timedelta. Only datetime.datetime does.
    def AddHour(self, target_date, og_time):
        return_val = datetime.combine(target_date, og_time)
        return_val += timedelta(hours=1)
        return_val = return_val.time()
        return return_val














