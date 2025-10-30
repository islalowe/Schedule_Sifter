// import { Router } from 'express';
// import { consumeJoinRoomToken } from '../services/MagicLinks.js';
// import { Room } from '../models/Room.js';

// const r = Router();

// r.get('/', async (req, res) => {
//   const token = String(req.query.ml || '');
//   if (!token) return res.status(400).send('Missing token');

//   const ml = await consumeJoinRoomToken(token);
//   if (!ml) return res.status(400).send('Invalid or expired link');

//   if (!req.user) {
//     req.session.postLoginJoin = { roomId: ml.roomId.toString() };
//     return res.redirect('/auth/google');
//   }

//   const room = await Room.findById(ml.roomId);
//   if (!room) return res.status(404).send('Room not found');

//   const exists = room.members.some(m => m.userId.toString() === req.user._id.toString());
//   if (!exists) room.members.push({ userId: req.user._id, role: 'member', joinedAt: new Date() });
//   await room.save();

//   return res.redirect(`${process.env.CLIENT_ORIGIN}/rooms/${room._id.toString()}`);
// });

// export default r;
