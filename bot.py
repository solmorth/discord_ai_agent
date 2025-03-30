import discord
import requests
import os

from logging import getLogger
from message_handler import Handler

logging = getLogger('discord.agent')


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


client = discord.Client(intents=intents)
message_handler = Handler(client=client, webhook_url=N8N_WEBHOOK_URL)

@client.event
async def on_ready():
      logging.info(
      'Ready! Invite URL: %s',
      discord.utils.oauth_url(
        client.application_id,
        permissions=discord.Permissions(
          read_messages=True,
          send_messages=True,
          create_public_threads=True,
        ),
        scopes=['bot'],
      ),
    )

@client.event
async def on_message(message):
  await message_handler.handle_message(message)

client.run(TOKEN)