from pydantic import BaseModel


class PreprocessedOrder(BaseModel):
    """
        Preprocessed order contains the information related to the order
        but includes the features that are added from cache and
        the hour of the day
    """
    is_retail: int
    avg_preparation_time: float
    hour_of_day: int
