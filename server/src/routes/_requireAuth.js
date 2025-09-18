// src/routes/_requireAuth.js
export function requireAuth(req, res, next) {
    if (!req.user) return res.status(401).json({ error: 'unauthorized' });
    next();
  }
  