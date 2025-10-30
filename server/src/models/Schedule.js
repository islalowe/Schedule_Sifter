// server/src/models/Schedule.js
import { Schema, model } from 'mongoose';

const IntervalSchema = new Schema(
  {
    start: { type: Date, required: true },   // ← Date, not String
    end:   { type: Date, required: true },
    label: { type: String, default: 'Busy' },
  },
  { _id: false }
);

const ScheduleSchema = new Schema(
  {
    userId:   { type: Schema.Types.ObjectId, ref: 'User', required: true, index: true },
    type:     { type: String, enum: ['default', 'last', 'room'], required: true, index: true },
    name:     { type: String, required: true, default: 'Default' },
    roomId:   { type: Schema.Types.ObjectId, ref: 'Room' },
    tz:       { type: String, default: 'America/Los_Angeles' }, // display/anchor tz
    intervals:{ type: [IntervalSchema], default: [] },
  },
  { timestamps: true }
);

ScheduleSchema.index({ userId: 1, name: 1 }, { unique: true });

export const Schedule = model('Schedule', ScheduleSchema);
