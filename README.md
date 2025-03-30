# Discord Bot with YouTube video summarization

A Discord bot that can extract and process YouTube video subtitles and provide webhook integration with n8n for further processing.

## Features

- **Message Handling**: Responds to mentions and processes commands
- **Command System**: Built-in command handling system
- **YouTube Integration**: Extracts subtitles from YouTube videos
- **n8n Webhook Integration**: Sends data to n8n for further processing
- **Reaction Feedback**: Provides visual feedback with message reactions

## Commands

- `/commands` - Lists all available commands
- `/yt [YouTube URL]` - Extracts and processes subtitles from a YouTube video

## Setup

### Local Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/disbot.git
   cd disbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export DISCORD_BOT_TOKEN=your_discord_bot_token
   export N8N_WEBHOOK_URL=your_n8n_webhook_url
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

### Docker Setup

1. Create a .env file (and add it to your .gitignore):
```
DISCORD_BOT_TOKEN=your_discord_bot_token
N8N_WEBHOOK_URL=your_n8n_webhook_url
```

2. Build and run the Docker container:
```bash
docker-compose up -d
```

## How it Works

1. The bot listens for messages that @mention it
2. When mentioned, it reacts with 👀 to acknowledge receipt
3. If the message contains a command (e.g., `/yt`), it processes that command
4. For YouTube URLs, it extracts subtitles and sends them to n8n for processing
5. For non-command messages, it forwards them to n8n for general processing

## Configuration

Configure the bot by modifying the available commands in message_handler.py:

```python
self.available_commands = ['/commands', '/yt']
```

Add additional commands by extending the `_handle_command` method in the `Handler` class.


## Requirements

- Python 3.10+
- discord.py
- requests
- YouTube API access (for subtitle extraction)
