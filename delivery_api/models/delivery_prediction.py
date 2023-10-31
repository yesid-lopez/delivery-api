from pydantic import BaseModel


class DeliveryPrediction(BaseModel):
    """
    Delivery duration time in minutes
    """
    delivery_duration: float
