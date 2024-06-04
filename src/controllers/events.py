# Core imports
from fastapi import APIRouter, Request, Depends, Header

from core.fastapi.middlewares import LocalizationRoute
from core.fastapi.dependencies import (
    TranslateJsonResponse
)

# App imports
from schemas import (
    Event,
    CreateEventRequest,
    Langs,
)

from models import EventType
from services import EventServices

# Python imports
from typing import List

router = APIRouter()


@router.post(
    "",
    response_class=TranslateJsonResponse,
    response_model=Event,
)
async def create_event(
        request: Request,
        schema: CreateEventRequest,
        accept_language: Langs = Header("tr"),
        event_type: EventType = Header(...),
):
    return await EventServices().create_event(event_type=event_type, schema=schema)
