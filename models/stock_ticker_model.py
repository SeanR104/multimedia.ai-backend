from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date

from system.database import Base


class StockTickerModel(Base):
    __tablename__ = 'stock_tickers'

    stock_ticker_id = Column(Integer, primary_key=True)
    company_detail_id = Column(Integer, ForeignKey('company_details.company_detail_id'), nullable=False)
    ticker_symbol = Column(String(10), nullable=False)
    stock_ticker_active = Column(Boolean, nullable=False)
    last_updated_profile = Column(Date, nullable=True)
    start_use_date = Column(Date, nullable=True)
    end_use_date = Column(Date, nullable=True)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
