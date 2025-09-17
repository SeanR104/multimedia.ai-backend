from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, DOUBLE_PRECISION, BigInteger

from system.database import Base


class PriceOptionModel(Base):
    __tablename__ = 'price_options'

    stock_option_id = Column(BigInteger, ForeignKey('stock_options.stock_option_id'), nullable=False)
    last_trade_price = Column(Numeric(15, 5), nullable=False)
    day_high_price = Column(Numeric(15, 5), nullable=False)
    day_low_price = Column(Numeric(15, 5), nullable=False)
    day_volume = Column(Integer, nullable=False)
    day_vwap = Column(Numeric(15, 5), nullable=False)
    last_tradeutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    bid_price = Column(Numeric(15, 5), nullable=False)
    bid_size = Column(Integer, nullable=False)
    ask_price = Column(Numeric(15, 5), nullable=False)
    ask_size = Column(Integer, nullable=False)
    open_interest = Column(Integer, nullable=False)
    implied_volatility = Column(DOUBLE_PRECISION, nullable=False)
    last_updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    previous_bid_price = Column(Numeric(15, 5), nullable=False)
    previous_ask_price = Column(Numeric(15, 5), nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
