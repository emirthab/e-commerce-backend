from sqlalchemy import Column, DateTime, func
from datetime import datetime, date


class Serializable():
    def serialize(self):
        d = {}
        for column in self.__table__.columns:
            if isinstance(getattr(self, column.name), (datetime, date)):
                d[column.name] = getattr(self, column.name).isoformat()
            else:
                d[column.name] = getattr(self, column.name)
                
        for relationship in self.__mapper__.relationships:
            if relationship.key in self.__dict__:
                value = getattr(self, relationship.key)
                if relationship.uselist:  # One-to-Many or Many-to-Many relationship
                    d[relationship.key] = [item.serialize() for item in value]
                else:  # Many-to-One or One-to-One relationship
                    d[relationship.key] = value.serialize() if value else None

        return d
