from pydantic import BaseModel, Field
from typing import Optional


class CurrentUser(BaseModel):
    id: int = Field(None, description="Id")
    is_authenticated: bool = Field(None, description="IsAuthenticated")
    role: str = Field("user", description="Role")
    email: str = Field(None, description="Email")
    phone: Optional[str] = Field(None, description="Phone")
    full_name: str = Field(None, description="FullName")
