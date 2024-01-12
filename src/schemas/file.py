from pydantic import BaseModel, Field
from datetime import datetime


class FileSchema(BaseModel):
    id: int = Field(...)
    show_name: str = Field(...)
    file_path: str = Field(...)
    extension: str = Field(...)
    size: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    download_url: str = Field(...)

    class Config:
        from_attributes = True


class UploadFileFromUrlSchema(BaseModel):
    url: str = Field(...)
