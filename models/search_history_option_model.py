from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, Date, Numeric, BigInteger

from system.database import Base


class SearchHistoryOptionModel(Base):
    __tablename__ = 'search_history_options'

    search_history_option_id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    ticker_symbol = Column(String(10), nullable=False)
    option_type = Column(String(10), nullable=False)
    expiration_date = Column(Date, nullable=False)
    strike_price = Column(Numeric(15, 5), nullable=False)
    api_searched = Column(Boolean, nullable=False)
    api_skip = Column(Boolean, nullable=False)
    lookup_count = Column(Integer, nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
