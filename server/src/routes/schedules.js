// server/src/routes/schedules.js
import { Router } from 'express';
import { z } from 'zod';
import { Schedule } from '../models/Schedule.js';
import { compareRoom } from '../../../archive/services/compare.js';
import { Room } from '../../../archive/services/Room.js';
import { requireAuth } from './_requireAuth.js';

// can use .datetime() 
const scheduleSchema = z.object({
  type: z.enum(['default', 'last', 'room']),
  roomId: z.string().optional(),
  tz: z.string().min(1), // e.g. "America/Los_Angeles"
  intervals: z.array(z.object({
    start: z.string().min(1),     // ISO coming from client
    end: z.string().min(1),
    label: z.string().optional()
  }))
});

const r = Router();

r.put('/me', requireAuth, async (req, res) => {
  const parsed = scheduleSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json(parsed.error);

  const { type, roomId, tz, intervals } = parsed.data;

  // 1) Convert ISO strings → Date objects
  const normalizedIntervals = [];
  for (const it of intervals) {
    const start = new Date(it.start);
    const end = new Date(it.end);
    if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
      return res.status(400).json({ error: 'Invalid date in intervals' });
    }
    if (end <= start) {
      return res.status(400).json({ error: 'Interval end must be after start' });
    }
    normalizedIntervals.push({
      start,
      end,
      label: it.label ?? 'Busy',
    });
  }

  // 2) Build the upsert key (one doc per user+type, and roomId if type==='room')
  const query = { userId: req.user._id, type };
  if (type === 'room') {
    if (!roomId) return res.status(400).json({ error: 'roomId is required when type is "room"' });
    query.roomId = roomId;
  }

  try {
    // 3) Save; timestamps are handled by the schema
    const doc = await Schedule.findOneAndUpdate(
      query,
      { $set: { tz: tz || 'America/Los_Angeles', intervals: normalizedIntervals } },
      { upsert: true, new: true }
    );
    res.json(doc); // Mongoose will serialize Dates back to ISO strings automatically
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to save schedule' });
  }
});

r.get('/me', requireAuth, async (req, res) => {
  const list = await Schedule.find({ userId: req.user._id }).limit(10);
  res.json(list);
});



// GET /api/schedules/me?type=default|last|room
r.get('/me', requireAuth, async (req, res) => {
  const filter = { userId: req.user._id };              // filter object looking for only this userId in the database
  if (req.query.type) {
    filter.type = req.query.type;                       // if there is a ?type, then that filter is added
  }     
  const list = await Schedule.find(filter).sort({ updatedAt: -1 }).limit(10);   // returns matching schedules, newest first, limited to 10
  res.json(list);
});

// GET /api/schedules/user/:id  (view another user’s schedules, if permitted)
r.get('/user/:id', requireAuth, async (req, res) => {
  // TODO: add authorization rules here
  const list = await Schedule.find({ userId: req.params.id }).sort({ updatedAt: -1 }).limit(10);
  res.json(list);
});

// GET /api/schedules/room/:roomId  (all member schedules saved with type='room' for that room)
r.get('/room/:roomId', requireAuth, async (req, res) => {
  const list = await Schedule.find({ roomId: req.params.roomId, type: 'room' }).limit(200);
  res.json(list);
});


// GET /api/schedules/room/:roomId  → all schedules saved with type='room' for that room
r.get('/room/:roomId', requireAuth, async (req, res) => {
  try {
    const roomId = req.params.roomId;

    // (Optional but safer) ensure requester is a member of the room
    // const room = await Room.findById(roomId);
    // if (!room) return res.status(404).json({ error: 'room not found' });
    // const isMember = room.members.some(m => m.userId.toString() === req.user._id.toString());
    // if (!isMember && room.ownerId.toString() !== req.user._id.toString()) {
    //   return res.status(403).json({ error: 'not a room member' });
    // }

    const list = await Schedule
      .find({ type: 'room', roomId })
      .populate('userId', 'name email picture'); // show who each schedule belongs to

    res.json(list);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'failed to fetch room schedules' });
  }
});





r.post('/rooms/:id/compare', requireAuth, async (req, res) => {
  const room = await Room.findById(req.params.id);
  if (!room) return res.status(404).json({ error: 'room not found' });

  const memberIds = (req.body && Array.isArray(req.body.members)) ? req.body.members : undefined;
  const result = await compareRoom(room._id.toString(), memberIds);
  res.json(result);
});

export default r;
