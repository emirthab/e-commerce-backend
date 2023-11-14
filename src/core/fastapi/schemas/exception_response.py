from pydantic import BaseModel

class ExceptionResponseSchema(BaseModel):
    error: str