from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.company_detail_schema import CompanyDetailSchema


class StockTickerBase(BaseModel):
    stock_ticker_id: int
    company_detail_id: int
    ticker_symbol: str
    stock_ticker_active: bool
    last_updated_profile: datetime
    start_use_date: datetime
    end_use_date: datetime
    createdutc: datetime
    updatedutc: datetime

    class Config:
        from_attribute = True


class StockTickerView(StockTickerBase):
    pass


class StockTickerSchema(BaseModel):
    ticker_symbol: str
    stock_ticker_active: bool
    last_updated_profile: Optional[datetime] = None
    start_use_date: Optional[datetime] = None
    end_use_date: Optional[datetime] = None

    company_detail: CompanyDetailSchema

    class Config:
        from_attribute = True


class StockTickerEdit(StockTickerBase):
    pass


class StockTickerRemove(StockTickerBase):
    pass
