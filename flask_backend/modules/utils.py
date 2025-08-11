# File I/O
# Time functions?

import json
from flask_backend.modules.event import Event
from flask_backend.modules.schedule import Schedule
from flask_backend.modules.daily_timetable import DailyTimetable
from datetime import datetime







# example_dictionary = {
#     "name": "sathiyajith",
#     "rollno": 56,
#     "cgpa": 8.6,
#     "phonenumber": "9976770500"
# }



# Function to send the results of the completed comparison to the results.json file
def write_results_to_json():
    # Serializing json
    json_object = json.dumps(results_dictionary, indent=4)
    # Writing to results.json
    with open("results.json", "w") as outfile:
        outfile.write(json_object)


# Function to load the details of a user schedule from the json file
#todo
def load_schedule_from_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    days = []
    for day in data["schedule"]:
        events = []
        for ev in day["events"]:
            events.append(Event(
                name=ev["name"],
                eventId=ev["eventId"],
                start=datetime.fromisoformat(ev["start"]),
                end=datetime.fromisoformat(ev["end"])
            ))
        days.append(DailyTimetable(events))
    return Schedule(days)
