// flask_backend/static/script.js

const $ = (id) => document.getElementById(id);

const example = {
  "schedule": [
    {
      "date": "2025-10-17",
      "events": [
        { "name": "Meeting", "eventId": 123, "start": "2025-10-17T09:00:00", "end": "2025-10-17T10:00:00" },
        { "name": "Class",   "eventId": 234, "start": "2025-10-17T11:00:00", "end": "2025-10-17T15:00:00" }
      ]
    },
    {
      "date": "2025-10-18",
      "events": [
        { "name": "Class",   "eventId": 456, "start": "2025-10-18T10:00:00", "end": "2025-10-18T15:00:00" }
      ]
    }
  ]
};

$("loadExample").onclick = () => {
  $("sched1").value = JSON.stringify(example, null, 2);
  $("sched2").value = JSON.stringify(example, null, 2);
};

$("compareBtn").onclick = async () => {
  $("status").textContent = "Comparing...";
  $("results").innerHTML = "";

  let s1, s2;
  try {
    s1 = JSON.parse($("sched1").value);
    s2 = JSON.parse($("sched2").value);
  } catch (e) {
    $("status").textContent = "Invalid JSON in one of the textareas.";
    return;
  }

  const payload = {
    schedule1: s1,
    schedule2: s2,
    days_to_check: Number($("minDays").value),
    granularity_hours: Number($("granularity").value),
  };

  try {
    const r = await fetch("/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await r.json();

    $("status").textContent = `Matches: ${data.matches.length}`;

    if (!data.matches.length) {
      $("results").innerHTML = "<div class='muted'>No common intervals found.</div>";
      return;
    }

    const rows = data.matches.map(m =>
      `<tr>
         <td>${m.date}</td>
         <td>${m.start.slice(11)}</td>
         <td>${m.end.slice(11)}</td>
         <td>${m.duration_minutes}</td>
       </tr>`
    ).join("");

    $("results").innerHTML = `
      <table>
        <thead>
          <tr><th>Date</th><th>Start</th><th>End</th><th>Duration (min)</th></tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>`;
  } catch (e) {
    $("status").textContent = "Error contacting API (open DevTools → Console).";
    console.error(e);
  }
};
