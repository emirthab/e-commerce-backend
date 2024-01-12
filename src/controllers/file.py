# Core imports
from fastapi import APIRouter, Request, Depends, UploadFile
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAuthenticated
)

# App imports
from schemas import FileSchema, UploadFileFromUrlSchema
from services import FileServices

# Pytohn imports

router = APIRouter()


@router.get(
    "/{file_id}",
    response_model=FileSchema,
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_file(file_id: int):
    return await FileServices().get_file(file_id=file_id)


@router.post(
    "",
    response_model=FileSchema,
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def upload_file(request: Request, file: UploadFile):
    return await FileServices().upload(file=file, user_id=0)


@router.post(
    "/from_url",
    response_model=FileSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def upload_file_from_url(request: Request, schema: UploadFileFromUrlSchema):
    return await FileServices().upload_from_url(url=schema.url, user_id=request.user.id)
