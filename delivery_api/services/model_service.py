import os

import numpy as np
from xgboost import XGBRegressor

from delivery_api.models.delivery_prediction import DeliveryPrediction
from delivery_api.models.preprocessed_order import PreprocessedOrder


class ModelService:
    """
    Service intended to load and make predictions to the trained model
    """

    def __init__(self):
        self._load_model()

    def _load_model(self) -> None:
        """
        Loads the model's checkpoint
        """
        model_weights_path = os.getenv("MODEL_WEIGHTS_PATH")
        assert model_weights_path, "Model weights path does not exist"

        self.model = XGBRegressor()
        self.model.load_model(model_weights_path)

    def predict(self, order: PreprocessedOrder) -> DeliveryPrediction:
        """
        Makes prediction to the model loaded based in the
        preprocessed order. The order contains all the required features
        for the model.

        :param order: preprocessed order
        :return: Delivery prediction that contains the delivery duration
        in seconds
        """
        data_for_prediction = np.array([
            order.is_retail,
            order.avg_preparation_time,
            order.hour_of_day
        ]).reshape(1, -1)

        delivery_duration = DeliveryPrediction(
            delivery_duration=self.model.predict(data_for_prediction)[0]
        )
        return delivery_duration
