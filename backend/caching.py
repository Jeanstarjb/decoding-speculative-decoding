import redis
import json
from typing import Optional

class RedisCache:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        """
        Initializes the RedisCache instance.

        Args:
            host (str): Redis server hostname.
            port (int): Redis server port.
            db (int): Redis database index.
        """
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def set(self, key: str, value: dict, ttl: int = 3600):
        """
        Stores a key-value pair in Redis with an optional time-to-live (TTL).

        Args:
            key (str): The key to store.
            value (dict): The value to store (will be serialized to JSON).
            ttl (int): Time-to-live in seconds (default: 3600 seconds).
        """
        serialized_value = json.dumps(value)
        self.client.setex(key, ttl, serialized_value)

    def get(self, key: str) -> Optional[dict]:
        """
        Retrieves a value from Redis by key.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[dict]: The deserialized value or None if the key does not exist.
        """
        serialized_value = self.client.get(key)
        if serialized_value is None:
            return None
        return json.loads(serialized_value)

# Example usage
if __name__ == "__main__":
    cache = RedisCache()
    cache.set("test_key", {"data": "test_value"}, ttl=300)
    print(cache.get("test_key"))