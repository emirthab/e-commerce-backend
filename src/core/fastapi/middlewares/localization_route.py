from enum import Enum
from fastapi.datastructures import DefaultPlaceholder
from starlette.routing import BaseRoute
from fastapi.types import IncEx
from core.fastapi.schemas import TranslatableStringType
from fastapi.routing import APIRoute
from typing import Optional, List, Sequence, Set, Type, Union, Any, Dict, Callable, get_origin
from fastapi import Depends, Request, Response
from core.helpers.redis import redis
import json
from pydantic.tools import parse_obj_as
from pydantic import BaseModel
from ..dependencies.translate_json_response import TranslateJsonResponse


class LocalizationRoute(APIRoute):
    """
    Route that localization response
    """

    def __init__(self, path: str, endpoint: Callable[..., Any], *, response_model: Any = ..., status_code: int | None = None, tags: List[str | Enum] | None = None, dependencies: Sequence[Depends] | None = None, summary: str | None = None, description: str | None = None, response_description: str = "Successful Response", responses: Dict[int | str, Dict[str, Any]] | None = None, deprecated: bool | None = None, name: str | None = None, methods: Set[str] | List[str] | None = None, operation_id: str | None = None, response_model_include: IncEx | None = None, response_model_exclude: IncEx | None = None, response_model_by_alias: bool = True, response_model_exclude_unset: bool = False, response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False, include_in_schema: bool = True, response_class: type[Response] | DefaultPlaceholder = ..., dependency_overrides_provider: Any | None = None, callbacks: List[BaseRoute] | None = None, openapi_extra: Dict[str, Any] | None = None, generate_unique_id_function: Callable[[APIRoute], str] | DefaultPlaceholder = ...) -> None:
        self.response_model_type = response_model

        super().__init__(path, endpoint, response_model=response_model, status_code=status_code, tags=tags, dependencies=dependencies, summary=summary, description=description, response_description=response_description, responses=responses, deprecated=deprecated, name=name, methods=methods, operation_id=operation_id, response_model_include=response_model_include, response_model_exclude=response_model_exclude, response_model_by_alias=response_model_by_alias,
                         response_model_exclude_unset=response_model_exclude_unset, response_model_exclude_defaults=response_model_exclude_defaults, response_model_exclude_none=response_model_exclude_none, include_in_schema=include_in_schema, response_class=response_class, dependency_overrides_provider=dependency_overrides_provider, callbacks=callbacks, openapi_extra=openapi_extra, generate_unique_id_function=generate_unique_id_function)

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)
            if not isinstance(response, TranslateJsonResponse):
                return response

            lang = request.headers.get('accept-language')
            
            data = response.body
            data_string = data.decode("utf-8")
            json_data = json.loads(data_string)

            _resp_model = self.response_model_type
            
            if (type(json_data) is list and not len(json_data)) or not _resp_model:
                return response
            
            parsed_data = parse_obj_as(_resp_model, json_data)

            return await response.translate_content(parsed_data, lang)

        return custom_route_handler
