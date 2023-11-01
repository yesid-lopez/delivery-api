import os

from pytest import fixture
from delivery_api.utils.redis_client import RedisClient


@fixture
def redis_client(mocker):
    # Mock the Redis connection object within the Redis client
    mock_redis_conn = mocker.patch('redis.Redis')
    mock_redis_conn.return_value.get.return_value = 'mocked_value'
    return mock_redis_conn.return_value


@fixture
def mock_env_vars(mocker):
    mocker.patch.dict(os.environ, {
        'REDIS_HOST': 'mocked_host',
        'REDIS_PORT': '1234',
    })


def test_get_successful(redis_client, mock_env_vars):
    # Arrange
    client = RedisClient()

    # Act
    result = client.get('mock_key')

    # Assert
    redis_client.get.assert_called_once_with('mock_key')
    assert result == 'mocked_value'
