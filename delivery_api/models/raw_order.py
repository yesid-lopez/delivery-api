from datetime import datetime

from pydantic import BaseModel


class RawOrder(BaseModel):
    """
    Raw order contains the raw information related to the order
    """
    venue_id: str
    time_received: datetime
    is_retail: int
