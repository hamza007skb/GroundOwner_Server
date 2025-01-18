from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class GroundResponseModel(BaseModel):
    id: int
    name: str
    email: str
    stadiumtype: str
    sportshours: str
    latitude: str
    longitude: str
    city: str
    address: str
    description: str
    rating: Optional[float] = None
    total_ratings: Optional[int] = None
    created_at: datetime
    country: str



class PitchResponseModel(BaseModel):
    ground_id: int
    name: str
    description: str
    length: str
    width: str
    price_per_60mins: str
    price_per_90mins: str
    created_at: datetime