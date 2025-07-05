# Discord MCP Server

A Model Context Protocol (MCP) server that enables AI models to interact with Discord through a standardized interface.

## Features

- Discord bot integration
- MCP-compliant API endpoints
- Simple API key authentication
- Message sending and retrieval
- Channel information
- Content moderation
- MCP Inspector integration for debugging
- Integration tests

## Setup

1. Create a Discord bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Add a bot to the application
   - Enable necessary intents (Message Content, Server Members)
   - Copy the bot token

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
HOST=localhost  # Optional, defaults to localhost
PORT=8000      # Optional, defaults to 8000
TEST_CHANNEL_ID=your_test_channel_id  # Required for running tests
```

## Running the Server

```bash
python run.py
```

## API Usage

The server exposes the following MCP tools:

1. `send_message`:
```json
{
    "api_key": "your_api_key",
    "tool": "send_message",
    "params": {
        "channel_id": "channel_id",
        "content": "Hello from MCP!"
    }
}
```

2. `get_messages`:
```json
{
    "api_key": "your_api_key",
    "tool": "get_messages",
    "params": {
        "channel_id": "channel_id",
        "limit": 100
    }
}
```

3. `get_channel_info`:
```json
{
    "api_key": "your_api_key",
    "tool": "get_channel_info",
    "params": {
        "channel_id": "channel_id"
    }
}
```

4. `search_messages`:
```json
{
    "api_key": "your_api_key",
    "tool": "search_messages",
    "params": {
        "channel_id": "channel_id",
        "query": "search term",
        "limit": 100
    }
}
```

5. `moderate_content`:
```json
{
    "api_key": "your_api_key",
    "tool": "moderate_content",
    "params": {
        "channel_id": "channel_id",
        "message_id": "message_id",
        "action": "delete"
    }
}
```

## Running Tests

```bash
pytest tests/
```

## Security Notes

- Keep your Discord bot token secure
- Use strong API keys
- Monitor the audit logs
- Follow Discord's rate limits and terms of service

## License

MIT 