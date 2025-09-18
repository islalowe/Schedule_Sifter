import { Schema, model } from 'mongoose';

const Interval = new Schema({
  start: String,   // ISO strings
  end: String,
  label: String
}, { _id: false });

const ScheduleSchema = new Schema({
  userId: { type: Schema.Types.ObjectId, ref: 'users', required: true, index: true },
  type: { type: String, enum: ['default', 'last', 'room'], required: true, index: true },
  roomId: { type: Schema.Types.ObjectId, ref: 'rooms' },
  tz: { type: String, default: 'UTC' },
  intervals: { type: [Interval], default: [] },
  updatedAt: { type: Date, default: () => new Date() }
});

export const Schedule = model('schedules', ScheduleSchema);
