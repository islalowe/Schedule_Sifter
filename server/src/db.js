import mongoose from 'mongoose';
import env from './env.js';

let isConnected = false;

export async function connectDb() {
  if (isConnected) return; // prevent multiple calls
  await mongoose.connect(env.mongoUri);

  mongoose.connection.on('connected', () => {
    console.log('✓ MongoDB connected');
  });

  mongoose.connection.on('error', (err) => {
    console.error('MongoDB connection error:', err);
  });

  isConnected = true;
}
