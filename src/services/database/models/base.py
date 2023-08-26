from datetime import datetime
import uuid
from typing import Optional, Any, Dict

from sqlalchemy import (
    BigInteger, 
    text, 
    DateTime, 
    func, 
    Integer, 
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    
    __abstract__: bool = True
    
    @declared_attr # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    def __repr__(self) -> str:
        params = ', '.join(
            f'{attr}={value!r}' 
            for attr, value in self.__dict__.items() 
            if not attr.startswith('_')
        )
        return f'{type(self).__name__}({params})'
    
    def as_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    
class ModelWithID:
    """Base model class that represents ID with an integer type"""
    
    id: Mapped[Optional[int]] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    
    
class ModelWithTime:
    
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=func.now(),
        server_default=func.now()
    )
    
    
class ModelWithUUID:
    """BaseUUID model class that represents ID with an UUID type"""
    
    id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text('gen_random_uuid()'),
        index=True,
        nullable=False
    )