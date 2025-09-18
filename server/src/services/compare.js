import axios from 'axios';
import { env } from '../env.js';

export async function compareRoom(roomId, memberIds) {
  const { data } = await axios.post(
    `${env.flaskUrl}/compare`,
    { roomId, memberIds },
    { timeout: 10000 }
  );
  return data;
}
