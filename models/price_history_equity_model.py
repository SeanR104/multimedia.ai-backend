from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Date

from system.database import Base


class PriceHistoryEquityModel(Base):
    __tablename__ = 'price_history_equities'

    stock_ticker_id = Column(Integer, ForeignKey('stock_tickers.stock_ticker_id'), Nullable=False)
    last_trade_price = Column(Numeric(15, 5), Nullable=False)
    close_bid_price = Column(Numeric(15, 5), Nullable=False)
    close_bid_size = Column(Integer, Nullable=False)
    close_ask_price = Column(Numeric(15, 5), Nullable=False)
    close_ask_size = Column(Integer, Nullable=False)
    day_high_price = Column(Numeric(15, 5), Nullable=False)
    day_low_price = Column(Numeric(15, 5), Nullable=False)
    fiftytwo_week_high = Column(Numeric(15, 5), Nullable=False)
    fiftytwo_week_low = Column(Numeric(15, 5), Nullable=False)
    previous_close = Column(Numeric(15, 4), Nullable=False)
    last_tradeutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), Nullable=False)
    last_trade_date = Column(Date, Nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), Nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), Nullable=False)
