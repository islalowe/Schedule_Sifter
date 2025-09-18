import mongoose from 'mongoose';
import env from './env.js';

// Named export (so index.js can do: import { connectDb } from './db.js')
export async function connectDb() {
  await mongoose.connect(env.mongoUri);

  mongoose.connection.on('connected', () => {
    console.log('✓ MongoDB connected');
  });

  mongoose.connection.on('error', (err) => {
    console.error('MongoDB connection error:', err);
  });
}
