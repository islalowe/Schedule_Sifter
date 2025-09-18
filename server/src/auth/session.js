import session from 'express-session';
import MongoStore from 'connect-mongo';
import { env } from '../env.js';

export const sessionMw = session({
  name: 'ssid',
  secret: env.sessionSecret,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    secure: false,        // set true when behind HTTPS/proxy
    sameSite: 'lax',
    maxAge: 1000 * 60 * 60 * 24 * 7
  },
  store: MongoStore.create({ mongoUrl: env.mongoUri })
});
