from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Time, Date

from system.database import Base


class MarketHolidayModel(Base):
    __tablename__ = 'market_holidays'

    market_holiday_id = Column(Integer, primary_key=True)
    holiday_date = Column(Date, nullable=False)
    local_timezone = Column(String(50), nullable=False)
    close_local_tz = Column(Time, nullable=True)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
