from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from system.database import Base


class ApiKeyModel(Base):
    __tablename__ = 'api_keys'

    api_key_id = Column(Integer, primary_key=True)
    key_value = Column(String(128), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    last_used_utc = Column(DateTime(timezone=True), nullable=True)
    revokedutc = Column(DateTime(timezone=True), nullable=True)
