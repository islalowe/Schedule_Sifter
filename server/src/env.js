import 'dotenv/config';

function required(name) {
  const v = process.env[name];
  if (!v) throw new Error(`Missing env ${name}`);
  return v;
}

export const env = {
  port: Number(process.env.PORT ?? 4000),
  mongoUri: required('MONGO_URI'),
  sessionSecret: required('SESSION_SECRET'),
  appBaseUrl: required('APP_BASE_URL'),
  clientOrigin: required('CLIENT_ORIGIN'),
  flaskUrl: required('FLASK_URL'),
  google: {
    clientId: required('GOOGLE_CLIENT_ID'),
    clientSecret: required('GOOGLE_CLIENT_SECRET'),
    callbackUrl: required('GOOGLE_CALLBACK_URL')
  },
  dataKeyB64: required('DATA_KEY_BASE64')
};

export default env;