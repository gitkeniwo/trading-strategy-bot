#!/usr/bin/env python3
import requests
from pathlib import Path

# Read bot token from .env
env_vars = {}
with open('.env') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            env_vars[key.strip()] = value.strip()

bot_token = env_vars.get('TELEGRAM_BOT_TOKEN')

print("=" * 60)
print("Get Telegram Channel ID")
print("=" * 60)
print("\nInstructions:")
print("1. Create a channel in Telegram")
print("2. Add your bot as administrator with 'Post Messages' permission")
print("3. Send a message in the channel")
print("4. Run this script\n")

url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
response = requests.get(url)
result = response.json()

if result.get('ok') and result.get('result'):
    print("Found updates:")
    for update in result['result']:
        # Check for channel posts
        if 'channel_post' in update:
            channel = update['channel_post']['chat']
            channel_id = channel['id']
            channel_title = channel.get('title', 'N/A')
            channel_username = channel.get('username', None)
            
            print(f"\n✅ Channel found!")
            print(f"   Title: {channel_title}")
            print(f"   Channel ID: {channel_id}")
            if channel_username:
                print(f"   Username: @{channel_username}")
                print(f"   Link: https://t.me/{channel_username}")
            
            print(f"\n📝 Update your .env file:")
            print(f"   TELEGRAM_CHAT_ID={channel_id}")
            break
    else:
        print("❌ No channel posts found")
        print("\nMake sure you:")
        print("1. Added bot as administrator")
        print("2. Posted a message in the channel")
        print("3. Bot has 'Post Messages' permission")
else:
    print("❌ No updates found")

print("\n" + "=" * 60)
