from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from datetime import datetime, timezone


@as_declarative()
class Base:
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
