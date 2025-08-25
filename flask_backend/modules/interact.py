# This file is used INSTEAD OF / TAKES THE PLACE OF simulate.py
# This file will:
#    read from schedule1.json and schedule2.json
#    instantiate comparer object to run comparison
#    convert the results returned by the comparison to json format via helper function
#    output the converted results to results.json

from flask_backend.modules.comparer import Comparer
import json
from pathlib import Path 
from datetime import datetime
from flask_backend.modules.event import Event
from flask_backend.modules.daily_timetable import DailyTimetable
from flask_backend.modules.schedule import Schedule
from flask_backend.modules.comparer import Comparer

# BASE_DIR is the folder where *this script* lives: .../flask_backend/modules
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUT_PATH = DATA_DIR / "results.json"

# Step 1: file input / loading json into python 
with (DATA_DIR / "schedule1.json").open("r", encoding="utf-8") as f:
    sched1_data = json.load(f)
with (DATA_DIR / "schedule2.json").open("r", encoding="utf-8") as f2:
    sched2_data = json.load(f2) # (turning the file data into a python dict)

# test reading the open json
one_day = sched1_data["schedule"][0]
print("One day example:", one_day)
print("Day date:", one_day.get("date"))
print("Events count:", len(one_day.get("events", [])))
print("One event:", one_day["events"][0])



# Step 2: convert json to event
def event_from_json(ev: dict) -> Event:
    """
    keys: name, eventId, start, end (ISO strings).
    """
    ename = ev.get("name") or "Untitled"
    eid = ev.get("eventId") 
    start_dt = datetime.fromisoformat(ev["start"])
    end_dt   = datetime.fromisoformat(ev["end"])
    return Event(ename, eid, start_dt, end_dt)
# sanity check on a single event
sample_ev_json = one_day["events"][0]
sample_ev_obj  = event_from_json(sample_ev_json)
print("\nStep 2 check — Event object:")
print("type:", type(sample_ev_obj))
print("name:", getattr(sample_ev_obj, "name", "(no name)"))
print("id:",    getattr(sample_ev_obj, "event_id", "(no id attr)"))
print("start/end:", getattr(sample_ev_obj, "start", None), getattr(sample_ev_obj, "end", None))

# Parsing full day now
def day_to_daily_timetable(day_obj: dict) -> DailyTimetable:
    events = [event_from_json(e) for e in day_obj.get("events", [])]
    return DailyTimetable(events)
# sanity check
dt = day_to_daily_timetable(one_day)
print("\nStep 3 check — DailyTimetable size:", len(dt.get_events()))

# Parsing the whole schedule now
def schedule_from_json(data: dict) -> Schedule:
    day_objs = data["schedule"]               # list of {"date": "...", "events": [...]}
    days = [day_to_daily_timetable(d) for d in day_objs]
    return Schedule(days)

# sanity checks
s1 = schedule_from_json(sched1_data)
s2 = schedule_from_json(sched2_data)
print("\nStep 4 check — Schedule sizes:", len(s1.days_list), len(s2.days_list))


# Step 3: compare
comparer = Comparer()
# matching simulate.py defaults 
days_to_check = 21
granularity_hours = 1

common_free = comparer.compare_two_schedules(s1, s2, days_to_check, granularity_hours)

print("\nStep 5 — Comparer result:")
if common_free:
    print(f"Found {len(common_free)} common intervals.")
    for iv in common_free:
        print(f"{iv.start.date()} — {iv.start.time()} to {iv.end.time()}")
else:
    print("No common intervals were found.")


# Step 4: file output (results.json)
def interval_to_dict(interval) -> dict:
    start_dt = interval.start
    end_dt   = interval.end
    duration_minutes = int((end_dt - start_dt).total_seconds() // 60)
    return {
        "date": start_dt.date().isoformat(),
        "start": start_dt.isoformat(timespec="minutes"),
        "end": end_dt.isoformat(timespec="minutes"),
        "duration_minutes": duration_minutes
    }

results_obj = {
    "days_to_check": days_to_check,
    "granularity_hours": granularity_hours,
    "matches": [interval_to_dict(iv) for iv in (common_free or [])]
}


with OUT_PATH.open("w", encoding="utf-8") as out:
    json.dump(results_obj, out, indent=2)

print("Wrote:", OUT_PATH.resolve())
