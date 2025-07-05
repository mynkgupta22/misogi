import logging
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class MCPInspector:
    def __init__(self):
        self.requests: List[Dict[str, Any]] = []

    def log_request(self, request_data: Dict[str, Any]) -> bool:
        """Log a request for debugging purposes."""
        try:
            self.requests.append({
                "timestamp": datetime.now().isoformat(),
                "data": request_data
            })
            return True
        except Exception as e:
            logger.error(f"Failed to log request: {e}")
            return False

    def get_recent_requests(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent requests for inspection."""
        return self.requests[-limit:]

    def clear_requests(self) -> bool:
        """Clear all logged requests."""
        try:
            self.requests.clear()
            return True
        except Exception as e:
            logger.error(f"Failed to clear requests: {e}")
            return False 