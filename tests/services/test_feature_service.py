from unittest.mock import MagicMock

from pytest import fixture
from pytest import raises

from delivery_api.errors.venue_error import VenueError
from delivery_api.models.raw_order import RawOrder
from delivery_api.services.feature_service import FeatureService


@fixture()
def raw_order():
    raw_order = RawOrder(
        venue_id="mock_id",
        time_received="2006-10-20 09:50:01.897036",
        is_retail=1
    )
    yield raw_order


def test_get_avg_preparation_time_feature_valid(mocker, raw_order: RawOrder):
    # Arrange
    mock_redis_client = mocker.patch('delivery_api.services.feature_service.RedisClient')
    expected_avg_time = 15.0
    mock_redis_client.return_value.get.return_value = expected_avg_time
    feature_service = FeatureService(raw_order=raw_order)

    # Act
    result = feature_service.get_avg_preparation_time_feature()

    # Assert
    mock_redis_client.return_value.get.assert_called_once_with(raw_order.venue_id)
    assert result == expected_avg_time


def test_get_avg_preparation_time_feature_missing_venue(mocker, raw_order: RawOrder):
    # Arrange
    mock_redis_client = mocker.patch('delivery_api.services.feature_service.RedisClient')
    mock_redis_client.return_value.get.return_value = None
    feature_service = FeatureService(raw_order=raw_order)

    # Act
    with raises(VenueError) as exc_info:
        feature_service.get_avg_preparation_time_feature()

    # Assert
    assert "Venue does not exist in cache" in str(exc_info.value)


def test_get_hour_of_day_feature_valid(mocker, raw_order: RawOrder):
    # Arrange
    mock_redis_client = mocker.patch('delivery_api.services.feature_service.RedisClient')
    mock_redis_client.return_value.get.return_value = None
    feature_service = FeatureService(raw_order=raw_order)

    # Act
    hour = feature_service.get_hour_of_day_feature()

    # Assert
    assert hour == raw_order.time_received.hour


def test_preprocess_successful(mocker, raw_order: RawOrder):
    # Arrange
    mocker.patch('delivery_api.services.feature_service.RedisClient')
    feature_service = FeatureService(raw_order=raw_order)
    expected_avg_preparation_time = 20.2
    feature_service.get_avg_preparation_time_feature = MagicMock(return_value=expected_avg_preparation_time)

    # Act
    preprocess_order = feature_service.preprocess()

    # Assert
    assert preprocess_order.avg_preparation_time == expected_avg_preparation_time
    assert preprocess_order.hour_of_day == raw_order.time_received.hour
    assert preprocess_order.is_retail == raw_order.is_retail
