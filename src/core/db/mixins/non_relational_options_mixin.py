from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import inspect


class NonRelationalOptions():
    @classmethod
    def get_columns(cls):
        inspector = inspect(cls)
        columns = [column for column in inspector.columns]
        return (columns)
