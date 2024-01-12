# Core imports
from fastapi import APIRouter, Request, Depends, UploadFile
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAuthenticated
)

# App imports

# Pytohn imports

router = APIRouter()

@router.get(
    "/{user_id}",
    # response_model=FileSchema,
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def recommend(request: Request, user_id: int):
    return "TODO"
