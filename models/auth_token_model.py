from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship

from system.database import Base


class AuthTokenModel(Base):
    __tablename__ = 'auth_tokens'

    auth_token_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    auth_token = Column(UUID, nullable=False)
    auth_token_expirationutc = Column(DateTime(timezone=True), nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    user = relationship('UserModel')
