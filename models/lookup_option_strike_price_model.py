from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, Date

from system.database import Base


class LookupOptionStrikeModel(Base):
    __tablename__ = 'lookup_option_strike_prices'

    stock_ticker_id = Column(Integer, ForeignKey('stock_tickers.stock_ticker_id'), nullable=False)
    expiration_date = Column(Date, nullable=False)
    strike_price = Column(Numeric(15, 5), nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
