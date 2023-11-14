from typing import Optional, Tuple

import jwt
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from config import config
from core.fastapi.schemas.current_user import CurrentUser


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, Optional[CurrentUser]]:
        user_state = CurrentUser()
        authorization: str = conn.headers.get("Authorization")

        if not authorization:
            return False, user_state

        try:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, user_state
        except ValueError:
            return False, user_state

        if not credentials:
            return False, user_state

        try:
            payload = jwt.decode(
                credentials,
                config.JWT_SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
            )
            user_state = CurrentUser(**payload)
        except jwt.exceptions.PyJWTError:
            return False, user_state

        return True, user_state


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
