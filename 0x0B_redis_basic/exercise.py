class Cache:
    """Cache class that stores data in Redis and tracks history of calls."""

    def __init__(self):
        """Initialize Redis instance and flush database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return a generated key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """Retrieve data from Redis with optional conversion function."""
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """Retrieve string value from Redis."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieve integer value from Redis."""
        return self.get(key, fn=int)
