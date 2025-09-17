from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, Date, Numeric, BigInteger

from system.database import Base


class StockOptionModel(Base):
    __tablename__ = 'stock_options'

    stock_option_id = Column(BigInteger, primary_key=True)
    stock_ticker_id = Column(Integer, ForeignKey('stock_tickers.stock_ticker_id'), nullable=False)
    option_type = Column(String(10), nullable=False)
    expiration_date = Column(Date, nullable=False)
    strike_price = Column(Numeric(15, 5), nullable=False)
    underlying_shares = Column(Numeric(15, 5), nullable=False)
    is_deleted = Column(Boolean, nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
