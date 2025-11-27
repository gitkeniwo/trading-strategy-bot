#!/usr/bin/env python3
import sys
import requests

sys.path.insert(0, 'src')
from trading_strategy.config.settings import settings

bot_token = settings.telegram_bot_token
chat_id = settings.telegram_chat_id

print("=" * 60)
print("Telegram Bot Diagnostics")
print("=" * 60)

# 1. Check bot info
print("\n1. Checking bot validity...")
url = f"https://api.telegram.org/bot{bot_token}/getMe"
response = requests.get(url)
result = response.json()

if result.get('ok'):
    bot_info = result['result']
    print(f"✅ Bot is valid!")
    print(f"   Bot name: {bot_info.get('first_name')}")
    print(f"   Bot username: @{bot_info.get('username')}")
else:
    print(f"❌ Bot token is invalid!")
    print(f"   Error: {result}")
    sys.exit(1)

# 2. Check for updates (to see if you've messaged the bot)
print("\n2. Checking if you've started a conversation with the bot...")
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
response = requests.get(url)
result = response.json()

if result.get('ok') and result.get('result'):
    print(f"✅ Found {len(result['result'])} message(s)")
    
    # Get the chat ID from the first message
    for update in result['result']:
        if 'message' in update:
            msg_chat_id = update['message']['chat']['id']
            username = update['message']['chat'].get('username', 'N/A')
            first_name = update['message']['chat'].get('first_name', 'N/A')
            
            print(f"\n   Chat ID from messages: {msg_chat_id}")
            print(f"   Username: @{username}")
            print(f"   Name: {first_name}")
            
            # Compare with .env
            if str(msg_chat_id) == str(chat_id):
                print(f"   ✅ Chat ID matches your .env file!")
            else:
                print(f"   ⚠️  WARNING: This doesn't match your .env ({chat_id})")
                print(f"   Update your .env to use: TELEGRAM_CHAT_ID={msg_chat_id}")
            break
else:
    print("❌ No messages found!")
    print("\n   Action required:")
    print(f"   1. Open Telegram and search for: @{bot_info.get('username')}")
    print("   2. Click 'Start' or send any message to the bot")
    print("   3. Run this script again")
    sys.exit(1)

print("\n" + "=" * 60)
print("Diagnosis complete!")
print("=" * 60)
