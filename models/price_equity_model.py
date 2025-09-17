from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey

from system.database import Base


class PriceEquityModel(Base):
    __tablename__ = 'price_equities'

    stock_ticker_id = Column(Integer, ForeignKey('stock_tickers.stock_ticker_id'), nullable=False)
    last_trade_price = Column(Numeric(15, 5), nullable=False)
    bid_price = Column(Numeric(15, 5), nullable=False)
    bid_size = Column(Integer, nullable=False)
    ask_price = Column(Numeric(15, 5), nullable=False)
    ask_size = Column(Integer, nullable=False)
    day_high_price = Column(Numeric(15, 5), nullable=False)
    day_low_price = Column(Numeric(15, 5), nullable=False)
    fiftytwo_week_high = Column(Numeric(15, 5), nullable=False)
    fiftytwo_week_low = Column(Numeric(15, 5), nullable=False)
    previous_close = Column(Numeric(15, 4), nullable=False)
    last_tradeutc = Column(DateTime(timezone=True), nullable=False)
    post_market_price = Column(Numeric(15, 5), nullable=True)
    post_market_tradeutc = Column(DateTime(timezone=True), nullable=True)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
