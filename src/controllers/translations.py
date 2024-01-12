# Core imports
from fastapi import APIRouter, Request, Depends, Header
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAuthenticated,
    IsAdmin,
)

# App imports
from schemas import CreateTranslationRequestSchema, Langs
from core.helpers.redis import redis

# Python imports
from typing import List, Optional

router = APIRouter()


@router.get(
    "",
)
async def get_translation(
    request: Request,
    prefix: str,
    accept_language: Langs = Header("tr")
):
    text_content = await redis.get(f'i18n::{prefix}::{accept_language}')
    return text_content


@router.post(
    "",
)
async def add_translation(
    request: Request,
    schema: CreateTranslationRequestSchema,
):
    await redis.set(f'i18n::{schema.prefix}::{schema.lang}', schema.text_content, keepttl=True)
    return 200
