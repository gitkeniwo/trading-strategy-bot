#!/usr/bin/env python3
import os
import requests
from pathlib import Path

# Read .env
env_vars = {}
with open('.env') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            env_vars[key.strip()] = value.strip()

bot_token = env_vars.get('TELEGRAM_BOT_TOKEN')
chat_id = env_vars.get('TELEGRAM_CHAT_ID')

print(f"Bot token: {bot_token[:15]}...")
print(f"Chat ID: {chat_id}")
print(f"Chat ID type: {type(chat_id)}")

# Try sending a simple message
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

# Test with different payloads
print("\n" + "=" * 60)
print("Test 1: Simple text, no parse_mode")
print("=" * 60)

payload1 = {
    "chat_id": chat_id,
    "text": "Test message 1 - simple text"
}

response = requests.post(url, json=payload1)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

if not response.json().get('ok'):
    # Try with integer chat_id
    print("\n" + "=" * 60)
    print("Test 2: Integer chat_id")
    print("=" * 60)
    
    payload2 = {
        "chat_id": int(chat_id),
        "text": "Test message 2 - integer chat_id"
    }
    
    response = requests.post(url, json=payload2)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
