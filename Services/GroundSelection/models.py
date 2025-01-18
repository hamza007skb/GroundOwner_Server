from typing import Optional

from pydantic import BaseModel


class GroundListModel(BaseModel):
    id: int
    name: str
    address: str
    photo: Optional[str]