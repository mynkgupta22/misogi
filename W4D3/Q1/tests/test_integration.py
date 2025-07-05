import pytest
import os
from src.main import DiscordMCPServer

@pytest.mark.asyncio
class TestDiscordMCP:
    @pytest.fixture
    async def server(self):
        """Create a test server instance."""
        server = DiscordMCPServer()
        yield server
        await server.stop()

    async def test_send_message(self, server):
        """Test sending a message."""
        result = await server.handle_request({
            "api_key": "test_key",
            "tool": "send_message",
            "params": {
                "channel_id": os.getenv("TEST_CHANNEL_ID", "your_test_channel_id"),
                "content": "Test message from MCP"
            }
        })
        assert result["success"] is True
        assert "message_id" in result

    async def test_get_messages(self, server):
        """Test getting messages."""
        result = await server.handle_request({
            "api_key": "test_key",
            "tool": "get_messages",
            "params": {
                "channel_id": os.getenv("TEST_CHANNEL_ID", "your_test_channel_id"),
                "limit": 5
            }
        })
        assert result["success"] is True
        assert "messages" in result
        assert isinstance(result["messages"], list)

    async def test_invalid_api_key(self, server):
        """Test authentication with invalid API key."""
        result = await server.handle_request({
            "api_key": "invalid_key",
            "tool": "send_message",
            "params": {
                "channel_id": "123",
                "content": "This should fail"
            }
        })
        assert result["success"] is False
        assert "Invalid API key" in result["error"] 