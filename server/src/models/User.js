import { Schema, model } from 'mongoose';

const UserSchema = new Schema({
  email: { type: String, unique: true, index: true, required: true },
  name: String,
  picture: String,
  googleId: String,
  createdAt: { type: Date, default: () => new Date() }
});

export const User = model('users', UserSchema);
