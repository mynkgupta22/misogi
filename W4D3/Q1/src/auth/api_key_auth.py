import logging
from typing import Set

logger = logging.getLogger(__name__)

class APIKeyAuth:
    def __init__(self):
        self.api_keys: Set[str] = set()
        # Add a default test key
        self.add_api_key("test_key")

    def add_api_key(self, key: str) -> bool:
        """Add a new API key."""
        try:
            self.api_keys.add(key)
            logger.info(f"Added new API key")
            return True
        except Exception as e:
            logger.error(f"Failed to add API key: {e}")
            return False

    def remove_api_key(self, key: str) -> bool:
        """Remove an API key."""
        try:
            self.api_keys.remove(key)
            logger.info(f"Removed API key")
            return True
        except KeyError:
            logger.error(f"API key not found")
            return False
        except Exception as e:
            logger.error(f"Failed to remove API key: {e}")
            return False

    def validate_key(self, key: str) -> bool:
        """Validate an API key."""
        return key in self.api_keys 