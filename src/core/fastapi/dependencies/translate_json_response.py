from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask
from core.fastapi.schemas import TranslatableStringType
from typing import Any, Dict
from core.helpers.redis import redis
import json
from pydantic import BaseModel
from datetime import datetime, date


class TranslateJsonResponse(JSONResponse):
    def __init__(self, content: Any, status_code: int = 200, headers: Dict[str, str] | None = None, media_type: str | None = None, background: BackgroundTask | None = None) -> None:
        self.original_content = content
        print(content)
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: Any) -> bytes:
        enco = lambda obj: (
            obj.isoformat()
            if isinstance(obj, datetime)
            or isinstance(obj, date)
            else None
        )
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            default=enco,
        ).encode("utf-8")

    async def translate_content(self, content, lang='tr'):
        tasks = []

        def add_task(value):
            if type(value) is TranslatableStringType:
                tasks.append(value)
            elif type(value) is list:
                for v in value:
                    add_task(v)
            elif isinstance(value, BaseModel):
                for key, value in value:
                    add_task(value)
            else:
                ...

        add_task(content)

        redis_keys = [f'i18n::{task.x}::Langs.{lang}' for task in tasks]
        new_data = await redis.mget(redis_keys)

        for task, new_value in zip(tasks, new_data):
            if not new_value:
                continue
            task.x = new_value.decode('utf-8')

        result = [item.dict() for item in content] if type(
            content) is list else content.dict()

        return TranslateJsonResponse(
            result,
            status_code=self.status_code,
            background=self.background
        )
