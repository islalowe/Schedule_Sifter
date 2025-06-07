# The Comparer class contains the schedule comparison functionality

from modules.time_interval import TimeInterval
from datetime import datetime, time, date, timedelta
from typing import List


class Comparer:
    def __init__(self):
        pass



    # This method compares two given schedules and returns a list of common free TimeInterval objects.
    # todo should the schedules be sorted? would the events ever get out of order?
    def CompareTwoSchedules(self, s1, s2, days_to_check = 7, min_hours = 1):
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
        for day in range(num_search_days):
            print('comparing a day, using a nested loop')
            # This holds one-day-only comparison results
            day_common_free_time: List[TimeInterval] = []
            day_common_free_time = self.CompareTwoForOneDay(s1, s2, min_hours, day)
            # Add the time intervals returned by the one-day comparison to the total comparison result 
            common_free_time.extend(day_common_free_time)
        # Return the result of the schedule comparison
        return common_free_time    



    def CompareTwoForOneDay(self, s1, s2, min_hours: int, day: int):
            hour = 0
            prev_interval_end_time = 0
            today = date.today()
            # Instantiate a TimeInterval with start and end times at 00
            target_date = today + timedelta(days=day)
            free_time_interval = TimeInterval(time(0, 0), time(0, 0), target_date)
            # This holds comparison results for one day only
            day_common_free_time: List[TimeInterval] = []

            s1_curr_event_tracker = 0
            s2_curr_event_tracker = 0
            # Start with the first events
            s1.curr_event = s1.days_list[s1_curr_event_tracker]
            s2.curr_event = s2.days_list[s2_curr_event_tracker]

            while hour < 24:
                # todo check to see what happens if events start and end on the same hour mark
                # If an event starts, free time ends.
                if (s1.curr_event.start == hour or s2.curr_event.start == hour):
                    # update curr event tracker
                    if (s1.curr_event.start == hour):
                        s1_curr_event_tracker += 1
                    else: 
                        s2_curr_event_tracker += 1
                    # Make sure the time interval passes the minimum hours threshold
                    if (free_time_interval.end - free_time_interval.start >= min_hours):
                        # Send the completed interval
                        day_common_free_time.extend(free_time_interval)

                        # Now, we are in the middle of an event. Time passes until *both* schedules have no running events.
                        # This loop ends once both schedule's current events end.
                        end_time = max(s1.curr_event.end, s2.curr_event.end)
                        while hour < end_time:    # Hour climbs from 0 to 24
                            hour += 1

                        # Now, the event ended for both. Free time may resume.
                        prev_interval_end_time = hour
                        free_time_interval.start = hour
                    
                # If an event has not started this hour, The free time interval does not end
                # so we increment the end of the free time interval by 1 hour
                else:
                    # Convert to datetime
                    dt = datetime.combine(target_date, free_time_interval.end)
                    # Add 1 hour 
                    dt += timedelta(hours=1)
                    # Set it back
                    free_time_interval.end = dt.time()
                hour += 1   # Either way, an hour passes.
            return day_common_free_time










