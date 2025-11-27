# Telegram Bot Setup Guide

This guide will walk you through setting up a Telegram bot for receiving trading strategy notifications.

## Prerequisites

- Telegram account (download Telegram app or use web version)
- 10 minutes of setup time

## Step 1: Create a Bot with @BotFather

1. **Open Telegram** and search for `@BotFather` (official bot by Telegram)

2. **Start a conversation** with @BotFather by clicking "Start" or typing `/start`

3. **Create a new bot** by typing `/newbot`

4. **Choose a name** for your bot (e.g., "My Trading Strategy Bot")
   - This is the display name users will see

5. **Choose a username** for your bot (must end in "bot")
   - Example: `my_trading_strategy_bot`
   - Must be unique across all Telegram bots

6. **Save your bot token**
   - @BotFather will send you a token that looks like:
     ```
     1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567
     ```
   - ⚠️ **IMPORTANT**: Keep this token secret! Anyone with this token can control your bot.
   - Save this as `TELEGRAM_BOT_TOKEN`

## Step 2: Get Your Chat ID

You need your Chat ID to tell the bot where to send messages.

### Method 1: Using @userinfobot (Easiest)

1. **Search for** `@userinfobot` in Telegram

2. **Start a conversation** with @userinfobot

3. The bot will immediately send you your user information, including your **Chat ID**
   - It will look like: `123456789` (a number)

4. **Save this number** as `TELEGRAM_CHAT_ID`

### Method 2: Using Telegram API (Alternative)

1. **Send a message** to your bot (search for it by the username you created)
   - Send any message like "Hello"

2. **Open this URL** in your browser (replace `YOUR_BOT_TOKEN` with your actual token):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```

3. **Find your Chat ID** in the JSON response:
   ```json
   {
     "result": [{
       "message": {
         "chat": {
           "id": 123456789
         }
       }
     }]
   }
   ```

4. **Copy the number** from `"id"` field

## Step 3: Configure Locally (for testing)

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** and add your credentials:
   ```env
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567
   TELEGRAM_CHAT_ID=123456789
   ```

3. **Test the connection** (optional):
   ```bash
   python -c "
   from trading_strategy.config.settings import settings
   from trading_strategy.notifications.telegram import TelegramNotifier

   notifier = TelegramNotifier(settings.telegram_bot_token, settings.telegram_chat_id)
   notifier.test_connection()
   "
   ```

   You should receive a test message in Telegram!

## Step 4: Configure GitHub Actions Secrets

To run the bot on GitHub Actions, you need to add your credentials as secrets.

1. **Go to your GitHub repository**

2. **Click on "Settings"** (repository settings, not your account settings)

3. **In the left sidebar**, click "Secrets and variables" → "Actions"

4. **Click "New repository secret"**

5. **Add `TELEGRAM_BOT_TOKEN`**:
   - Name: `TELEGRAM_BOT_TOKEN`
   - Secret: Your bot token from Step 1
   - Click "Add secret"

6. **Add `TELEGRAM_CHAT_ID`**:
   - Click "New repository secret" again
   - Name: `TELEGRAM_CHAT_ID`
   - Secret: Your chat ID from Step 2
   - Click "Add secret"

## Step 5: Verify Setup

### Local Verification

Run the trading strategy locally to test:

```bash
python -m trading_strategy.main
```

You should receive a notification in Telegram!

### GitHub Actions Verification

1. **Go to "Actions"** tab in your repository

2. **Select "Trading Strategy Bot"** workflow

3. **Click "Run workflow"** → "Run workflow" (manual trigger)

4. **Wait for the workflow** to complete

5. **Check Telegram** for the notification

## Troubleshooting

### Bot doesn't send messages

**Check 1**: Verify your token is correct
```bash
# This should return bot information
curl https://api.telegram.org/botYOUR_TOKEN/getMe
```

**Check 2**: Verify chat ID is correct
- Make sure it's a number (no quotes)
- Try Method 2 from Step 2 if Method 1 didn't work

**Check 3**: Ensure you've sent at least one message to the bot
- Bots can't initiate conversations; you must message them first

### "Unauthorized" error

- Your bot token is incorrect
- Double-check you copied the entire token from @BotFather

### Messages not received

- Verify your chat ID is correct
- Check that you've started a conversation with your bot
- Make sure your Telegram account can receive messages from bots

### GitHub Actions not working

- Verify secrets are added correctly (no extra spaces or quotes)
- Check workflow logs in Actions tab for specific errors
- Ensure `.env` file is NOT committed to git (it should be in `.gitignore`)

## Security Best Practices

1. **Never commit `.env`** to git
   - It's already in `.gitignore`
   - Never share your bot token publicly

2. **Use GitHub Secrets** for production
   - Don't put credentials in code or workflow files

3. **Regenerate token if compromised**
   - Use `/revoke` command with @BotFather
   - Create a new bot if needed

4. **Limit bot permissions**
   - Your bot only needs to send messages
   - Don't add it to groups unless needed

## Next Steps

- ✅ Bot is configured
- ✅ Test messages working
- ✅ Ready to receive trading signals!

See [README.md](../README.md) for running the full trading strategy.
