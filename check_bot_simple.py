#!/usr/bin/env python3
import os
import requests
from pathlib import Path

# Read .env file
env_path = Path('.env')
if not env_path.exists():
    print("❌ .env file not found!")
    exit(1)

env_vars = {}
with open('.env') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            env_vars[key.strip()] = value.strip()

bot_token = env_vars.get('TELEGRAM_BOT_TOKEN')
chat_id = env_vars.get('TELEGRAM_CHAT_ID')

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
    bot_username = bot_info.get('username')
else:
    print(f"❌ Bot token is invalid!")
    print(f"   Error: {result}")
    exit(1)

# 2. Check for updates
print("\n2. Checking if you've started a conversation with the bot...")
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
response = requests.get(url)
result = response.json()

if result.get('ok') and result.get('result'):
    print(f"✅ Found {len(result['result'])} message(s)")
    
    # Get the chat ID from the first message
    found_chat = False
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
                found_chat = True
            else:
                print(f"   ⚠️  WARNING: Chat ID mismatch!")
                print(f"   Your .env has: {chat_id}")
                print(f"   Should be: {msg_chat_id}")
                print(f"\n   Fix: Update your .env file:")
                print(f"   TELEGRAM_CHAT_ID={msg_chat_id}")
            break
    
    if not found_chat and result.get('result'):
        print("\n   ⚠️  No matching chat found")
else:
    print("❌ No messages found!")
    print("\n   🔧 Action required:")
    print(f"   1. Open Telegram and search for: @{bot_username}")
    print("   2. Click 'Start' or send any message (like 'hello')")
    print("   3. Run this script again")
    print("\n   Your current chat ID in .env:", chat_id)
    exit(1)

print("\n" + "=" * 60)
print("Diagnosis complete!")
print("=" * 60)
