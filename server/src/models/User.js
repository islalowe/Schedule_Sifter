import { Schema, model } from 'mongoose';

const UserSchema = new Schema(
  {
    googleId: { type: String, index: true },
    email:    { type: String, unique: true, index: true, required: true },
    name:     { type: String, index: true },
    picture:  String,
    timezone: { type: String, default: 'America/Los_Angeles' }, 
  },
  { timestamps: true } // Mongoose will maintain createdAt/updatedAt
);

export const User = model('User', UserSchema); 
