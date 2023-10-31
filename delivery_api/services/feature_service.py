import logging

from delivery_api.models.preprocessed_order import PreprocessedOrder
from delivery_api.models.raw_order import RawOrder
from delivery_api.utils.redis_client import RedisClient

logger = logging.getLogger(__name__)


class FeatureService:
    """
    Feature service is created to define the feature
    engineering steps. Including preprocessing steps
    and getting features from cache for a faster
    inference
    """

    def __init__(self, raw_order: RawOrder):
        self.redis_client = RedisClient()
        self.raw_order = raw_order

    def get_avg_preparation_time_feature(self) -> float:
        """
        Based on a venue id from the order, retrieves the average preparation
        time for the venue
        :return: average preparation time
        """
        avg_preparation_time = self.redis_client.get(self.raw_order.venue_id)
        return avg_preparation_time

    def get_hour_of_day_feature(self) -> int:
        """
        hour of the day based on the order's time received

        :return: hour of the day
        """
        hour_of_day = self.raw_order.time_received.hour
        return hour_of_day

    def preprocess(self) -> PreprocessedOrder:
        """
        Triggers the whole feature engineering process.
        Every feature engineering step should be listed here in
        order to be executed

        :return: order preprocessed ready to be sent to the model
        """
        avg_preparation_time = self.get_avg_preparation_time_feature()
        hour_of_day = self.get_hour_of_day_feature()

        preprocessed_order = PreprocessedOrder(
            avg_preparation_time=avg_preparation_time,
            hour_of_day=hour_of_day,
            is_retail=self.raw_order.is_retail,
        )
        return preprocessed_order
