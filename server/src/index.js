import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import cookieParser from 'cookie-parser';

import { connectDb } from './db.js';
import { env } from './env.js';
import { sessionMw } from './auth/session.js';
import { passport } from './auth/google.js';

import authRoutes from './routes/auth.js';
import roomsRoutes from './routes/rooms.js';
import schedulesRoutes from './routes/schedules.js';
import joinRoutes from './routes/join.js';

(async () => {
  await connectDb();

  const app = express();

  app.use(helmet());
  app.use(cors({ origin: env.clientOrigin, credentials: true }));
  app.use(express.json());
  app.use(cookieParser());
  app.use(sessionMw);
  app.use(passport.initialize());
  app.use(passport.session());

  app.use('/auth', authRoutes);
  app.use('/rooms', roomsRoutes);
  app.use('/schedules', schedulesRoutes);
  app.use('/join', joinRoutes);

  // Optional helper: after login, client can redirect here if you store a post-login route
  app.get('/post-login', (req, res) => {
    const join = req.session?.postLoginJoin;
    if (!join) return res.redirect(env.clientOrigin);
    const id = join.roomId;
    delete req.session.postLoginJoin;
    res.redirect(`${env.clientOrigin}/rooms/${id}`);
  });

  app.listen(env.port, () => {
    console.log(`API running on http://localhost:${env.port}`);
  });
})();
