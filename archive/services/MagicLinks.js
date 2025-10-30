// import { randomBytes, createHash } from 'crypto';
// import { MagicLink } from '../models/MagicLink.js';

// function sha256(buf) {
//   return createHash('sha256').update(buf).digest('hex');
// }

// export async function issueJoinRoomLink(roomId, ttlMinutes = 10) {
//   const token = randomBytes(32);
//   const tokenHash = sha256(token);
//   const expiresAt = new Date(Date.now() + ttlMinutes * 60 * 1000);

//   await MagicLink.create({
//     purpose: 'join_room',
//     tokenHash,
//     roomId,
//     expiresAt,
//     used: false
//   });

//   return token.toString('base64url'); // return raw token (b64url) for URL/QR
// }

// export async function consumeJoinRoomToken(rawB64) {
//   try {
//     const raw = Buffer.from(rawB64, 'base64url');
//     const tokenHash = sha256(raw);
//     const ml = await MagicLink.findOne({ tokenHash });
//     if (!ml || ml.used || ml.expiresAt < new Date()) return null;
//     ml.used = true;
//     await ml.save();
//     return ml;
//   } catch {
//     return null;
//   }
// }
