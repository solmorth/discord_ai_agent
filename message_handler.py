from logging import getLogger
from youtube import YouTube
import requests

logging = getLogger("discord.agent")


class Handler:
    def __init__(self, client, webhook_url):
        self.client = client
        self.webhook_url = webhook_url
        self.available_commands = ["/commands", "/yt"]

    async def handle_message(self, message):
        """
        Handle incoming messages.
        """
        # Check if the message is from the bot itself
        if message.author.bot:
            return

        # Check if the message mentions the bot
        if self.client.user.mentioned_in(message):  # Fixed method name here
            logging.info("New message received")
            await message.add_reaction("👀")
            # Clean the content of the message
            clean_content = message.content.replace(
                f"<@{self.client.user.id}>", ""
            ).strip()
            if clean_content in ["", " ", None]:
                await self.send_message_to_discord(
                    message.channel.id, "Please provide a command or message."
                )
            elif any(clean_content.startswith(cmd) for cmd in self.available_commands):
                command = clean_content.split()[0]
                await self._handle_command(message.channel.id, command, clean_content)
            else:
                # If not a command, send to n8n webhook
                response = self._send_to_n8n_webhook(clean_content)
                if response.status_code == 200:
                    await self.send_message_to_discord(
                        message.channel.id, "Message sent to n8n webhook successfully."
                    )
                else:
                    await self.send_message_to_discord(
                        message.channel.id, "Failed to send message to n8n webhook."
                    )

    async def _handle_command(self, channel_id, command, content):
        """
        Handle various bot commands.
        """
        logging.info(f"Command received: {command}")
        match command:
            case "/commands":
                n = "\n".join(self.available_commands)
                await self.send_message_to_discord(
                    channel_id, f"Available commands: \n{n}"
                )
            case "/yt":
                await self._handle_yt_command(content, channel_id)

    async def _handle_yt_command(self, content, channel_id):
        try:
            url = content.split(" ")[1]
        except IndexError:
            await self.send_message_to_discord(
                channel_id, "Please provide a YouTube URL."
            )
            return
        if not url or not url.startswith("https://www.youtube.com/watch"):
            await self.send_message_to_discord(
                channel_id, "Please provide a YouTube URL."
            )
            return

        await self.send_message_to_discord(
            channel_id, "Fetching subtitles for provided URL"
        )
        yt = YouTube(url)
        subtitles = yt.get_subtitles()
        if subtitles:
            await self.send_message_to_discord(
                channel_id, "Subtitles found, trying to summarize"
            )
            # Send the subtitles to n8n webhook
            response = self._send_to_n8n_webhook(
                f"Sumarize the following subtitles:\n{subtitles}"
            )
            if response.status_code == 200:
                await self.send_message_to_discord(
                    channel_id, "Subtitles sent to n8n webhook successfully."
                )
            else:
                await self.send_message_to_discord(
                    channel_id, "Failed to send subtitles to n8n webhook."
                )
        else:
            await self.send_message_to_discord(
                channel_id, "No subtitles available for this video."
            )

    def _send_to_n8n_webhook(self, data):
        payload = {"content": data}

        # Send the payload to N8N webhook
        response = requests.post(self.webhook_url, payload, timeout=10, verify=False)
        if response.status_code == 200:
            logging.info("Data sent to n8n webhook successfully.")
        else:
            logging.error(
                f"Failed to send data to n8n webhook. Status code: {response.status_code}"
            )
        return response

    async def send_message_to_discord(self, channel_id, message):
        """
        Send a message to Discord.
        """
        channel = self.client.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            logging.error("Channel not found")
