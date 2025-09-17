from datetime import datetime
from pydantic import BaseModel

from schemas.stock_ticker_schema import StockTickerSchema


class PriceEquityBase(BaseModel):
    stock_ticker_id: int
    last_trade_price: float
    bid_price: float
    bid_size: int
    ask_price: float
    ask_size: int
    day_high_price: float
    day_low_price: float
    fiftytwo_week_high: float
    fiftytwo_week_low: float
    previous_close: float
    last_tradeutc: datetime
    post_market_price: float
    post_market_tradeutc: datetime
    createdutc: datetime
    updatedutc: datetime

    class Config:
        from_attribute = True


class PriceEquityView(PriceEquityBase):
    pass


class PriceEquitySchema(BaseModel):
    last_trade_price: float
    bid_price: float
    bid_size: int
    ask_price: float
    ask_size: int
    day_high_price: float
    day_low_price: float
    fiftytwo_week_high: float
    fiftytwo_week_low: float
    previous_close: float
    last_tradeutc: datetime
    post_market_price: float
    post_market_tradeutc: datetime

    stock_ticker: StockTickerSchema

    class Config:
        from_attribute = True


class PriceEquityEdit(PriceEquityBase):
    pass


class PriceEquityDelete(PriceEquityBase):
    pass
