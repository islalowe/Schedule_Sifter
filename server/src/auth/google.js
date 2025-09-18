import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
import { env } from '../env.js';
import { User } from '../models/User.js';

passport.serializeUser((user, done) => done(null, user._id.toString()));

passport.deserializeUser(async (id, done) => {
  try {
    const u = await User.findById(id);
    done(null, u || false);
  } catch (e) {
    done(e);
  }
});

passport.use(new GoogleStrategy({
  clientID: env.google.clientId,
  clientSecret: env.google.clientSecret,
  callbackURL: env.google.callbackUrl
}, async (_accessToken, _refreshToken, profile, done) => {
  try {
    const email = profile.emails?.[0]?.value?.toLowerCase();
    if (!email) return done(null, false);

    let user = await User.findOne({ email });
    if (!user) {
      user = await User.create({
        email,
        name: profile.displayName,
        picture: profile.photos?.[0]?.value,
        googleId: profile.id
      });
    }
    done(null, user);
  } catch (e) {
    done(e);
  }
}));

export { passport };
