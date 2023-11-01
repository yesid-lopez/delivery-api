import logging
import os

import uvicorn
from fastapi import FastAPI, HTTPException

from delivery_api.errors.venue_error import VenueError
from delivery_api.models.delivery_prediction import DeliveryPrediction
from delivery_api.models.raw_order import RawOrder
from delivery_api.services.feature_service import FeatureService
from delivery_api.services.model_service import ModelService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    try:
        feature_service = FeatureService(raw_order)
        preprocessed_order = feature_service.preprocess()

        model_service = ModelService()
        delivery_duration = model_service.predict(preprocessed_order)

        logger.info(
            "Delivery duration predicted successfully",
            extra={
                "order": raw_order,
                "delivery_duration": delivery_duration
            }
        )
        return delivery_duration
    except VenueError as e:
        logger.error("Error on the venue", extra={"error message": str(e)})
        raise HTTPException(status_code=400, detail=str(e)) from e


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
