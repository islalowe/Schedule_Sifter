const el = (id) => document.getElementById(id);

let currentRoomId = null;    // should not always be null


/* This section handles putting a logi gate in front of all functionality */
async function getMe() {
  const res = await fetch('/api/auth/me', { credentials: 'include' });
  if (!res.ok) return null;
  return res.json();
}
function setAuthedUI(user) {
  // Toggle nav buttons
  document.getElementById('btnLogin')?.classList.add('hidden');
  document.getElementById('btnLogout')?.classList.remove('hidden');
  // Optional: show name/pic somewhere
  // document.querySelector('#welcome')?.textContent = user.name;
}
window.addEventListener('DOMContentLoaded', async () => {
  const me = await getMe();
  if (me) setAuthedUI(me);
  else setGuestUI();
  // Wire “Who am I?” for convenience
  document.getElementById('btnMe')?.addEventListener('click', async () => {
    const user = await getMe();
    if (!user) return alert('Not logged in');
    alert(`${user.name} <${user.email}>`);
  });
  // Logout
  document.getElementById('btnLogout')?.addEventListener('click', async () => {
    await fetch('/auth/logout', { method: 'POST', credentials: 'include' });
    location.reload();
  });
});


// Helper for JSON fetch with cookies
async function api(path, options = {}) {
  const res = await fetch(path, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options
  });
  if (!res.ok) {
    let msg = `${res.status} ${res.statusText}`;
    try { const j = await res.json(); msg += `: ${j.error || JSON.stringify(j)}`; } catch {}
    throw new Error(msg);
  }
  // some endpoints return images or redirects; default to json
  try { return await res.json(); } catch { return {}; }
}

// Auth
el('btnMe').onclick = async () => {
  try {
    const data = await api('/auth/me');
    alert(JSON.stringify(data, null, 2));
  } catch (e) { alert(e.message); }
};

el('btnLogout').onclick = async () => {
  try {
    await api('/auth/logout', { method: 'POST' });
    alert('Logged out');
  } catch (e) { alert(e.message); }
};

// Rooms
el('btnCreateRoom').onclick = async () => {
  try {
    const name = el('roomName').value || 'New Room';
    const room = await api('/rooms', { method: 'POST', body: JSON.stringify({ name }) });
    currentRoomId = room._id;
    el('roomInfo').textContent = `Room created: ${room._id}`;
    el('btnShowQR').disabled = false;
    el('btnCompare').disabled = false;
  } catch (e) { alert(e.message); }
};

el('btnShowQR').onclick = async () => {
  if (!currentRoomId) return;
  try {
    const { qrDataUrl } = await api(`/rooms/${currentRoomId}/qr`, { method: 'POST' });
    el('qr').src = qrDataUrl;
  } catch (e) { alert(e.message); }
};

// Schedule
el('btnSaveSchedule').onclick = async () => {
  try {
    const tz = el('tz').value || 'America/Los_Angeles';
    const s = el('startIso').value;
    const e = el('endIso').value;
    const intervals = s && e ? [{ start: s, end: e, label: 'demo' }] : [];
    const res = await api('/schedules/me', {
      method: 'PUT',
      body: JSON.stringify({ type: 'default', tz, intervals })
    });
    el('scheduleMsg').textContent = `Saved. intervals=${res.intervals?.length ?? 0}`;
  } catch (err) { el('scheduleMsg').textContent = err.message; }
};

// Compare
el('btnCompare').onclick = async () => {
  if (!currentRoomId) return;
  try {
    const data = await api(`/schedules/rooms/${currentRoomId}/compare`, {
      method: 'POST',
      body: JSON.stringify({})
    });
    el('compareOut').textContent = JSON.stringify(data, null, 2);
  } catch (e) { el('compareOut').textContent = e.message; }
};



async function fetchMySchedules() {
  const res = await fetch('/api/schedules/me', { credentials: 'include' });
  const data = await res.json();
  renderSchedules('#mySchedules', data);
}

async function fetchRoomSchedules(roomId) {
  const res = await fetch(`/api/schedules/room/${roomId}`, { credentials: 'include' });
  const data = await res.json();
  renderSchedules('#roomSchedules', data);
}

function renderSchedules(containerSelector, schedules) {
  const el = document.querySelector(containerSelector);
  if (!el) return;
  el.innerHTML = schedules.map(s => `
    <div class="card">
      <h3>${s.name ?? s.type} <small>(${s.tz})</small></h3>
      <p><em>Updated:</em> ${new Date(s.updatedAt || s.createdAt).toLocaleString()}</p>
      <table style="width:100%; border-collapse: collapse">
        <thead>
          <tr>
            <th style="text-align:left; border-bottom:1px solid #ddd;">Start</th>
            <th style="text-align:left; border-bottom:1px solid #ddd;">End</th>
            <th style="text-align:left; border-bottom:1px solid #ddd;">Label</th>
          </tr>
        </thead>
        <tbody>
          ${s.intervals.map(iv => `
            <tr>
              <td>${new Date(iv.start).toLocaleString(undefined, { timeZone: s.tz })}</td>
              <td>${new Date(iv.end).toLocaleString(undefined, { timeZone: s.tz })}</td>
              <td>${iv.label || 'Busy'}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `).join('');
}
