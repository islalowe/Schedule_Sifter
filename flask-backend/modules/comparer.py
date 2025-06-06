# The Comparer class contains the schedule comparison functionality

from modules.time_interval import TimeInterval
from datetime import datetime, time, date
from typing import List

class Comparer:
    def __init__(self):
        pass

    # This method compares two given schedules and returns a list of common free TimeInterval objects.
    # todo should the schedules be sorted? would the events ever get out of order?
    def CompareTwoSchedules(s1, s2, range = 7, size = 1):
        """
        Compare two schedules
        Args:
            s1 (Schedule): First schedule.
            s2 (Schedule): Second schedule.
            range (int): the number of days in the future to search through
            size (int): the number of hours that will be considered the minimum for a TimeInterval object to be returned

        Returns:
            List: the shared TimeInterval objects.
        """

        # This is the product of the search, it returned to the user.
        common_free_time: List[TimeInterval] = []     # clear the list

        # Find the shortest among s1, s2, and range
        num_search_days = min(s1.size(), s2.size(), range)

        # Iterate through the two schedules together
        # Add every consecutive hour that is free for both schedules to a TimeInterval object (may happen multiple times per day)
        for day in range(num_search_days):
            print('comparing a day, using a nested loop')
            # Instantiate a TimeInterval with start and end times at 00
            free_time_interval = TimeInterval(time(0, 0), time(0, 0), day.date)
            hour = 0
            prev_interval_end_time = 0
            # Start with the first events
            s1.curr_event = s1.at(0)
            s2.curr_event = s2.at(0)
            while hour < 24:
                # todo check to see what happens if events start and end on the same hour mark
                # If an event starts, free time ends.
                if (s1.currEvent.start == hour or s2.currEvent.start == hour):
                    # Make sure the time interval passes the minimum size threshold
                    if (free_time_interval.end - free_time_interval.start >= size):
                        # Send the completed interval
                        common_free_time.append(free_time_interval)

                        # Now, we are in the middle of an event. Time passes until *both* schedules have no running events.
                        # This loop ends once both schedule's current events end.
                        end_time = max(s1.curr_event.end, s2.curr_event.end)
                        while hour < end_time:    # Hour climbs from 0 to 24
                            hour += 1

                        # Now, the event ended for both. Free time may resume.
                        prev_interval_end_time = hour
                        free_time_interval.start = hour

                #todo handle incrementing the curr_events
                    
                # If an event has not started this hour
                else:
                    # The free time interval does not end
                    free_time_interval.end += 1
                hour += 1   # Either way, an hour passes.










