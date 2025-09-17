from datetime import datetime

from pydantic import BaseModel

from schemas.stock_ticker_schema import StockTickerSchema


class CompanyEarningSchema(BaseModel):
    book_value: float
    eps_forward: float
    eps_trailing: float
    dividend_rate_trailing: float
    dividend_date: datetime
    earnings_date_last: datetime
    earnings_date_next_start: datetime
    earnings_date_next_end: datetime
    market_cap: int
    shares_outstanding: int
    day_volume: int
    day_volume_average_10_days: int
    day_volume_average_3_months: int
    stock_ticker: StockTickerSchema
