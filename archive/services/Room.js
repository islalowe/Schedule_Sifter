import { Schema, model } from 'mongoose';

const Member = new Schema({
  userId: { type: Schema.Types.ObjectId, ref: 'users', required: true },
  role: { type: String, enum: ['owner', 'member'], default: 'member' },
  canShareDetail: { type: String, enum: ['freebusy', 'titles'], default: 'freebusy' },
  joinedAt: { type: Date, default: () => new Date() }
}, { _id: false });

const RoomSchema = new Schema({
  ownerId: { type: Schema.Types.ObjectId, ref: 'users', required: true },
  name: { type: String, required: true },
  members: { type: [Member], default: [] },
  createdAt: { type: Date, default: () => new Date() }
});

export const Room = model('rooms', RoomSchema);
