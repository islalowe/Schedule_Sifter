# flask_backend/app.py
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from .modules.event import Event
from .modules.daily_timetable import DailyTimetable
from .modules.schedule import Schedule
from .modules.comparer import Comparer

app = Flask(__name__)

# These are helpers to build domain objects 
def event_from_json(ev: dict) -> Event:
    # JSON uses: name, eventId, start, end (ISO strings)
    return Event(
        ev.get("name") or "Untitled",
        ev.get("eventId") or ev.get("id"),
        datetime.fromisoformat(ev["start"]),
        datetime.fromisoformat(ev["end"]),
    )

def day_to_dt(day: dict) -> DailyTimetable:
    events = [event_from_json(e) for e in day.get("events", [])]
    return DailyTimetable(events)

def schedule_from_json(data: dict) -> Schedule:
    # expects: {"schedule": [ {"date": "...", "events": [...]}, ... ]}
    days = [day_to_dt(d) for d in data["schedule"]]
    return Schedule(days)

def interval_to_dict(iv) -> dict:
    dur = int((iv.end - iv.start).total_seconds() // 60)
    return {
        "date": iv.start.date().isoformat(),
        "start": iv.start.isoformat(timespec="minutes"),
        "end": iv.end.isoformat(timespec="minutes"),
        "duration_minutes": dur,
    }

def unique_intervals(intervals):
    """Remove duplicates by (start,end) pair while preserving order."""
    seen = set()
    out = []
    for iv in intervals or []:
        key = (iv.start, iv.end)
        if key not in seen:
            seen.add(key)
            out.append(iv)
    return out

# ---------- routes ----------
@app.get("/")               # GET /  (serve the web page)
def home():
    return render_template("index.html")

@app.post("/compare")       # POST /compare  (accept JSON, return JSON)
def compare():
    payload = request.get_json(force=True)

    s1 = schedule_from_json(payload["schedule1"])
    s2 = schedule_from_json(payload["schedule2"])
    # these are knobs for algorithm
    days_to_check = int(payload.get("days_to_check", 7))
    granularity_hours = int(payload.get("granularity_hours", 1))

    comparer = Comparer()
    matches = comparer.compare_two_schedules(s1, s2, days_to_check, granularity_hours) or []

    return jsonify({
        "days_to_check": days_to_check,
        "granularity_hours": granularity_hours,
        "matches": [interval_to_dict(m) for m in matches],
    })

@app.get("/health")
def health():
    return {"ok": True}

if __name__ == "__main__":
    # run locally
    app.run(host="127.0.0.1", port=5001, debug=True)

