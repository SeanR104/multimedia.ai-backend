from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey

from system.database import Base


class SearchHistoryStockModel(Base):
    __tablename__ = 'search_history_stocks'

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    ticker_symbol = Column(String(10), nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
