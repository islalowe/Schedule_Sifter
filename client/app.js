const el = (id) => document.getElementById(id);

let currentRoomId = null;

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
