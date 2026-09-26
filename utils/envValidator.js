const logger = require('./logger');
const REQUIRED_VARS = [
  'DISCORD_TOKEN',
  'CLIENT_ID',
  'CLIENT_SECRET',
  'OWNER_ID',
  'MONGODB_URI'
];

function validateEnv() {
  const missing = [];

  for (const key of REQUIRED_VARS) {
    if (!process.env[key] || process.env[key].trim() === '') {
      missing.push(key);
    }
  }

  if (missing.length > 0) {
    logger.error('\n❌ [Error] Missing required environment variables in .env file:');
    for (const key of missing) {
      logger.error(`   - ${key}`);
    }
    logger.error('\nPlease populate these variables in your .env file and restart the bot.\n');
    process.exit(1);
  }

  if (!process.env.GUILD_ID || process.env.GUILD_ID.trim() === '') {
    logger.info('[Info] GUILD_ID is not specified. Slash commands will be deployed globally.');
  }

  if (!process.env.PORT) {
    logger.info('[Info] PORT is not specified. Defaulting to 3000.');
  }

  if (!process.env.CALLBACK_URL) {
    logger.info('[Info] CALLBACK_URL is not specified. Defaulting to http://localhost:3000/auth/callback.');
  }

  if (!process.env.BACKUP_WEBHOOK_URL) {
    logger.info('[Info] BACKUP_WEBHOOK_URL is not specified. Discord auto-backups will be disabled.');
  }
}

module.exports = validateEnv();
