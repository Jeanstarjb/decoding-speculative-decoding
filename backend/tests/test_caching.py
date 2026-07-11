import unittest
from unittest.mock import patch, MagicMock
from backend.caching import RedisCache

class TestRedisCache(unittest.TestCase):

    @patch('redis.StrictRedis')
    def setUp(self, mock_redis):
        self.mock_redis = mock_redis.return_value
        self.cache = RedisCache(host='localhost')

    def test_set_and_get(self):
        key = 'test_key'
        value = {'data': 'test_value'}
        ttl = 300

        self.cache.set(key, value, ttl)
        self.mock_redis.setex.assert_called_once_with(key, ttl, '{"data": "test_value"}')

        self.mock_redis.get.return_value = '{"data": "test_value"}'
        result = self.cache.get(key)
        self.assertEqual(result, value)

    def test_get_nonexistent_key(self):
        self.mock_redis.get.return_value = None
        result = self.cache.get('nonexistent_key')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()