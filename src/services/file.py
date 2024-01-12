import uuid
import os
import requests

from sqlalchemy import select
from fastapi import UploadFile
from firebase_admin import storage
from core.db import session, standalone_session

from models import File
from schemas import FileSchema
from errors import FileNotFoundException


class FileServices:
    def __init__(self):
        ...

    @standalone_session
    async def upload(self, file: UploadFile, user_id: int = None) -> File:
        show_name, extension = os.path.splitext(file.filename)
        path = str(uuid.uuid4()) + extension
        bucket = storage.bucket()
        blob = bucket.blob(path)
        blob.upload_from_file(file.file)
        blob.make_public()

        file = File(
            show_name=show_name,
            file_path=path,
            extension=extension,
            size=blob.size,
            created_by=user_id
        )
        session.add(file)
        await session.commit()
        await session.refresh(file)

        return file

    async def get_file(self, file_id: int) -> File:
        query = select(File).where(File.id == file_id)
        result = await session.execute(query)
        file = result.scalars().first()

        if not file:
            raise FileNotFoundException

        bucket = storage.bucket()
        blob = bucket.blob(file.file_path)
        blob.make_public()

        return file

    async def upload_from_url(self, url: str, user_id: int = None) -> File:
        response = requests.get(url)

        if response.status_code != 200:
            raise FileNotFoundException

        _, extension = os.path.splitext(url)
        path = str(uuid.uuid4()) + extension
        bucket = storage.bucket()
        blob = bucket.blob(path)
        blob.upload_from_string(response.content)
        blob.make_public()

        file = File(
            show_name=os.path.basename(url),
            file_path=path,
            extension=extension,
            size=blob.size,
            created_by=user_id
        )
        session.add(file)
        await session.commit()
        await session.refresh(file)

        return file
