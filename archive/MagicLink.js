// import { Schema, model } from 'mongoose';

// const MagicLinkSchema = new Schema({
//   purpose: { type: String, enum: ['signin', 'join_room'], required: true, index: true },
//   tokenHash: { type: String, required: true, index: true, unique: true },
//   roomId: { type: Schema.Types.ObjectId, ref: 'rooms' },
//   userId: { type: Schema.Types.ObjectId, ref: 'users' },
//   expiresAt: { type: Date, required: true }, // <-- remove "index: true" here
//   used: { type: Boolean, default: false, index: true },
//   createdAt: { type: Date, default: () => new Date() }
// });

// // a single TTL index
// MagicLinkSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 });

// export const MagicLink = model('magic_links', MagicLinkSchema);
