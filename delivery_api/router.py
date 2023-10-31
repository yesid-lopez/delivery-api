import logging
import os

import uvicorn
from fastapi import FastAPI

from delivery_api.models.delivery_prediction import DeliveryPrediction
from delivery_api.models.raw_order import RawOrder
from delivery_api.services.feature_service import FeatureService
from delivery_api.services.model_service import ModelService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    """
    Returns a hello world message
    :return: dict with a hello world message
    """
    return {"Hello": "World"}


@app.get("/healthcheck")
def healthcheck() -> dict[str, str]:
    """
    Returns a healthcheck validation
    :return: dict with a successful healthcheck message
    """
    return {"message": "The healthcheck was successful."}


@app.post("/predict")
def predict(raw_order: RawOrder) -> DeliveryPrediction:
    """
    Returns a delivery_duration inference based, for that
    it is needed to preprocess the features and then make
    the prediction to the model
    :param raw_order: RawOrder
    :return: delivery duration predicted
    """
    feature_service = FeatureService(raw_order)
    preprocessed_order = feature_service.preprocess()

    model_service = ModelService()
    return model_service.predict(preprocessed_order)


def run() -> None:
    """
    Bootstraps the delivery service
    """
    host = os.getenv("HOST", "127.0.0.1")
    reload = os.getenv("RELOAD", "False") == "True"
    uvicorn.run(
        "delivery_api.router:app",
        host=host,
        reload=reload,
    )
