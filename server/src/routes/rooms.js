// import { Router } from 'express';
// import QRCode from 'qrcode';
// import { Room } from '../models/Room.js';
// import { issueJoinRoomLink } from '../services/MagicLinks.js';
// import { requireAuth } from './_requireAuth.js';

// const r = Router();

// r.post('/', requireAuth, async (req, res) => {
//   const name = (req.body && req.body.name) || 'New Room';
//   const room = await Room.create({
//     ownerId: req.user._id,
//     name,
//     members: [{ userId: req.user._id, role: 'owner', joinedAt: new Date() }]
//   });
//   res.json(room);
// });

// r.get('/:id', requireAuth, async (req, res) => {
//   const room = await Room.findById(req.params.id);
//   if (!room) return res.status(404).json({ error: 'not found' });
//   res.json(room);
// });

// r.post('/:id/qr', requireAuth, async (req, res) => {
//   const token = await issueJoinRoomLink(req.params.id, 10);
//   const url = `${process.env.APP_BASE_URL}/join?ml=${token}`;
//   const dataUrl = await QRCode.toDataURL(url);
//   res.json({ url, qrDataUrl: dataUrl });
// });

// export default r;
