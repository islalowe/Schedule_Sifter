import { Router } from 'express';
import { passport } from '../auth/google.js';

const r = Router();

r.get('/google', passport.authenticate('google', { scope: ['openid', 'email', 'profile'] }));

r.get('/google/callback',
  passport.authenticate('google', { failureRedirect: '/auth/fail' }),
  (_req, res) => res.redirect(process.env.CLIENT_ORIGIN)
);

r.get('/me', (req, res) => {
  res.json({ user: req.user ?? null });
});

r.post('/logout', (req, res, next) => {
  req.logout(err => err ? next(err) : res.json({ ok: true }));
});

export default r;
