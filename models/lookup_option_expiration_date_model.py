from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Date

from system.database import Base


class LookupOptionExpirationModel(Base):
    __tablename__ = 'lookup_option_expiration_dates'

    stock_ticker_id = Column(Integer, ForeignKey('stock_tickers.stock_ticker_id'), nullable=False)
    expiration_date = Column(Date, nullable=False)
    strike_price_updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=True)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
