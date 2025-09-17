from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UUID

from system.database import Base


class SearchApiStatusModel(Base):
    __tablename__ = 'search_api_status'

    search_api_status_id = Column(Integer, primary_key=True)
    api_name = Column(String(50), nullable=False)
    platform_running = Column(String(25), nullable=False)
    is_running = Column(Boolean, nullable=False)
    run_uuid = Column(UUID, nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
