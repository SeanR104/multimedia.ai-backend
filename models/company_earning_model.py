from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, Numeric, BigInteger, ForeignKey, Date

from system.database import Base


class CompanyEarningModel(Base):
    __tablename__ = 'company_earnings'

    stock_ticker_id = Column(Integer, ForeignKey('stock_tickers.stock_ticker_id'), nullable=False)
    book_value = Column(Numeric(15, 5), nullable=False)
    eps_forward = Column(Numeric(15, 5), nullable=False)
    eps_trailing = Column(Numeric(15, 5), nullable=False)
    dividend_rate_trailing = Column(Numeric(15, 5), nullable=False)
    dividend_date = Column(Date, nullable=True)
    earnings_date_last = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=True)
    earnings_date_next_start = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=True)
    earnings_date_next_end = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=True)
    market_cap = Column(BigInteger, nullable=False)
    shares_outstanding = Column(BigInteger, nullable=False)
    day_volume = Column(BigInteger, nullable=False)
    day_volume_average_10_days = Column(BigInteger, nullable=False)
    day_volume_average_3_months = Column(BigInteger, nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
