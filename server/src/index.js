import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import cookieParser from 'cookie-parser';

import { connectDb } from './db.js';
import env from './env.js';
import { sessionMw } from './auth/session.js';
import { passport } from './auth/google.js';

import authRoutes from './routes/auth.js';
import roomsRoutes from './routes/rooms.js';
import schedulesRoutes from './routes/schedules.js';
import joinRoutes from './routes/join.js';

import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

(async () => {
  await connectDb();

  const app = express();

  // Core middleware
  app.use(helmet());
  app.use(cors({ origin: env.clientOrigin, credentials: true }));
  app.use(express.json());
  app.use(cookieParser());
  app.use(sessionMw);
  app.use(passport.initialize());
  app.use(passport.session());

  // Serve /client from project root: /Schedule_Sifter/client
  const clientDir = path.join(__dirname, '..', '..', 'client');
  // console.log('Serving client from:', clientDir);
  app.use(express.static(clientDir));
  app.get('/', (_req, res) => {
    res.sendFile(path.join(clientDir, 'index.html'));
  });

  // API routes
  app.use('/auth', authRoutes);
  app.use('/rooms', roomsRoutes);
  app.use('/schedules', schedulesRoutes);
  app.use('/join', joinRoutes);

  // Optional helper: after login redirect
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
