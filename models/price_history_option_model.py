from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Date, BigInteger

from system.database import Base


class PriceHistoryOptionModel(Base):
    __tablename__ = 'price_history_options'

    stock_option_id = Column(BigInteger, ForeignKey('stock_options.stock_option_id'), Nullable=False)
    close_price = Column(Numeric(15, 5), Nullable=False)
    close_high = Column(Numeric(15, 5), Nullable=False)
    close_low = Column(Numeric(15, 5), Nullable=False)
    close_volume = Column(Integer, Nullable=False)
    vwa_price = Column(Numeric(15, 5), Nullable=False)
    last_trade_date = Column(Date, Nullable=False)
    last_tradeutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), Nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), Nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), Nullable=False)
