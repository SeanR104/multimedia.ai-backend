from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, String, UUID

from system.database import Base


class SearchApiHistoryModel(Base):
    __tablename__ = 'search_api_history'

    search_api_history_id = Column(Integer, primary_key=True)
    api_name = Column(String(50), nullable=False)
    url_text = Column(String, nullable=False)
    url_parameters = Column(String, nullable=False)
    post_body = Column(String, nullable=False)
    http_status = Column(String(5), nullable=False)
    platform_running = Column(String(25), nullable=False)
    run_uuid = Column(UUID, nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
