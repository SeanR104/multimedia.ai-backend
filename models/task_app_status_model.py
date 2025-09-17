from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, UUID

from system.database import Base


class TaskAppStatusModel(Base):
    __tablename__ = 'task_app_status'

    task_app_status_id = Column(Integer, primary_key=True)
    task_app_name = Column(String(50), nullable=False)
    run_uuid = Column(UUID, nullable=False)
    task_app_status = Column(String(10), nullable=False)
    last_checkutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    terminate_requestutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=True)
    process_killedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=True)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
