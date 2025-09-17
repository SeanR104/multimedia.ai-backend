from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Date, DOUBLE_PRECISION, BigInteger

from system.database import Base


class PriceHistoryOptionInterestModel(Base):
    __tablename__ = 'price_history_options_interest'

    stock_option_id = Column(BigInteger, ForeignKey('stock_options.stock_option_id'), nullable=False)
    bid_price = Column(Numeric(15, 5), nullable=False)
    bid_size = Column(Integer, nullable=False)
    ask_price = Column(Numeric(15, 5), nullable=False)
    ask_size = Column(Integer, nullable=False)
    open_interest = Column(Integer, nullable=False)
    implied_volatility = Column(DOUBLE_PRECISION, nullable=False)
    last_update_date = Column(Date, nullable=False)
    last_updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
