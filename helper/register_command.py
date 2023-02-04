import os
import requests

# This is a script you keep to yourself and run locally each time 
# you want to create/update your application's commands

# global commands are cached and only update every hour
# url = f"https://discord.com/api/v8/applications/{APP_ID}/commands"

# while guild commands update instantly
# they"re much better for testing

BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
APP_ID = os.environ["DISCORD_APP_ID"]
GUILD_ID = os.environ["DISCORD_GUILD_ID"]


url = f"https://discord.com/api/v8/applications/{APP_ID}/guilds/{GUILD_ID}/commands"

json = {
  "name": "support",
  "type": 1,
  "description": "Ask for the very best of technical support",
  "options": [{
    "name": "question",
    "description": "Ask your question",
    "type": 3,
    "required": True
  }]
}

response = requests.post(url, headers={
  "Authorization": f"Bot {BOT_TOKEN}"
}, json=json)

print(response.json())