from pydantic import Field, BaseModel
from typing import Optional, List

from models import EventType, Event


class Event(BaseModel):
    id: int = Field(...)
    event_type: EventType = Field(...)
    product_id: int = Field(...)
    user_id: int = Field(...)

    class Config:
        from_attributes = True


class CreateEventRequest(BaseModel):
    product_id: int = Field(...)
    user_id: int = Field(...)

    class Config:
        from_attributes = True

