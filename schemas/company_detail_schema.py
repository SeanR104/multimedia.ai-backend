from datetime import datetime
from pydantic import BaseModel


class CompanyDetailBase(BaseModel):
    company_detail_id: int
    short_name: str
    long_name: str
    cik_code: str
    locale_name: str
    primary_exchange: str
    currency_type: str
    stock_type: str
    company_profile: str
    num_employees: int
    company_sector: str
    company_industry: str
    company_address1: str
    company_address2: str
    company_city: str
    company_state: str
    company_zip: str
    company_country: str
    company_website: str
    company_phone: str
    createdutc: datetime
    updatedutc: datetime

    class Config:
        from_attribute = True


class CompanyDetailView(CompanyDetailBase):
    pass


class CompanyDetailSchema(BaseModel):
    short_name: str
    long_name: str
    cik_code: str
    locale_name: str
    primary_exchange: str
    currency_type: str
    stock_type: str
    company_profile: str
    num_employees: int
    company_sector: str
    company_industry: str
    company_address1: str
    company_address2: str
    company_city: str
    company_state: str
    company_zip: str
    company_country: str
    company_website: str
    company_phone: str

    class Config:
        from_attribute = True


class CompanyDetailEdit(CompanyDetailBase):
    pass


class CompanyDetailRemove(CompanyDetailBase):
    pass
