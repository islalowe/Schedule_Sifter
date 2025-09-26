// server/src/models/Schedule.js
import { Schema, model } from 'mongoose';

const IntervalSchema = new Schema({
  start: { type: String, required: true },
  end:   { type: String, required: true },
  label: { type: String, default: 'Busy' },
}, { _id: false });

const ScheduleSchema = new Schema({
  userId:   { type: Schema.Types.ObjectId, ref: 'User', required: true, index: true },
  type:     { type: String, enum: ['default', 'last', 'room'], required: true, index: true },
  roomId:   { type: Schema.Types.ObjectId, ref: 'Room' },
  tz:       { type: String, default: 'America/Los_Angeles' },
  intervals:{ type: [IntervalSchema], default: [] },
}, { timestamps: true });

export const Schedule = model('Schedule', ScheduleSchema);
