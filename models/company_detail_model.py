from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text

from system.database import Base


class CompanyDetailModel(Base):
    __tablename__ = 'company_details'

    company_detail_id = Column(Integer, primary_key=True)
    short_name = Column(String(100), nullable=False)
    long_name = Column(String(100), nullable=False)
    cik_code = Column(String(12), nullable=False)
    locale_name = Column(String(4), nullable=False)
    primary_exchange = Column(String(25), nullable=False)
    currency_type = Column(String(4), nullable=False)
    stock_type = Column(String(10), nullable=False)
    company_profile = Column(Text, nullable=False)
    num_employees = Column(Integer, nullable=False)
    company_sector = Column(String(100), nullable=False)
    company_industry = Column(String(100), nullable=False)
    company_address1 = Column(String(100), nullable=False)
    company_address2 = Column(String(100), nullable=False)
    company_city = Column(String(100), nullable=False)
    company_state = Column(String(100), nullable=False)
    company_zip = Column(String(20), nullable=False)
    company_country = Column(String(56), nullable=False)
    company_website = Column(String(255), nullable=False)
    company_phone = Column(String(25), nullable=False)
    createdutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updatedutc = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
