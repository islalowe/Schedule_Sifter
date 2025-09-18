import { Router } from 'express';
import { z } from 'zod';
import { Schedule } from '../models/Schedule.js';
import { compareRoom } from '../services/compare.js';
import { Room } from '../models/Room.js';
import { requireAuth } from './_requireAuth.js';

const scheduleSchema = z.object({
  type: z.enum(['default', 'last', 'room']),
  roomId: z.string().optional(),
  tz: z.string(),
  intervals: z.array(z.object({
    start: z.string(),
    end: z.string(),
    label: z.string().optional()
  }))
});

const r = Router();

r.put('/me', requireAuth, async (req, res) => {
  const parsed = scheduleSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json(parsed.error);

  const { type, roomId, tz, intervals } = parsed.data;

  const query = { userId: req.user._id, type };
  if (type === 'room') query.roomId = roomId;

  const doc = await Schedule.findOneAndUpdate(
    query,
    { tz, intervals, updatedAt: new Date() },
    { upsert: true, new: true }
  );
  res.json(doc);
});

r.get('/me', requireAuth, async (req, res) => {
  const list = await Schedule.find({ userId: req.user._id }).limit(50);
  res.json(list);
});

r.post('/rooms/:id/compare', requireAuth, async (req, res) => {
  const room = await Room.findById(req.params.id);
  if (!room) return res.status(404).json({ error: 'room not found' });

  const memberIds = req.body && Array.isArray(req.body.members) ? req.body.members : undefined;
  const result = await compareRoom(room._id.toString(), memberIds);
  res.json(result);
});

export default r;
