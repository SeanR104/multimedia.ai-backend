from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime, UUID
from system.database import Base


class UserModel(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_uuid = Column(UUID, nullable=False)
    email_address = Column(String(254), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    user_is_enabled = Column(Boolean, nullable=False)
    user_is_deleted = Column(Boolean, nullable=False)
    user_role_type = Column(String(10), nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
