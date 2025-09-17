from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, field_validator, ValidationError

from utilities.utils import utils
from utilities.utils import OutputLogType


class Quote(BaseModel):
    preMarketChange: Optional[float]
    preMarketChangePercent: Optional[float]
    preMarketPrice: Optional[float]
    preMarketTime: Optional[int]

    postMarketChange: Optional[float]
    postMarketChangePercent: Optional[float]
    postMarketPrice: Optional[float]
    postMarketTime: Optional[int]

    language: Optional[str]
    region: Optional[str]
    quoteType: Optional[str]
    typeDisp: Optional[str]
    quoteSourceName: Optional[str]
    triggerable: Optional[bool]
    customPriceAlertConfidence: Optional[str]

    currency: Optional[str]
    exchange: Optional[str]
    shortName: Optional[str]
    marketState: Optional[str]
    longName: Optional[str]
    messageBoardId: Optional[str]
    market: Optional[str]

    regularMarketPrice: Optional[float]
    regularMarketChangePercent: Optional[float]
    gmtOffSetMilliseconds: Optional[int]
    exchangeTimezoneName: Optional[str]
    exchangeTimezoneShortName: Optional[str]
    esgPopulated: Optional[bool]

    regularMarketDayLow: Optional[float]
    regularMarketVolume: Optional[int]

    fiftyTwoWeekRange: Optional[str]
    fiftyTwoWeekHighChange: Optional[float]
    fiftyTwoWeekHighChangePercent: Optional[float]
    fiftyTwoWeekLow: Optional[float]
    fiftyTwoWeekHigh: Optional[float]
    fiftyTwoWeekChangePercent: Optional[float]

    dividendDate: Optional[int]
    earningsTimestamp: Optional[int]
    earningsTimestampStart: Optional[int]
    earningsTimestampEnd: Optional[int]

    trailingAnnualDividendRate: Optional[float]
    trailingPE: Optional[float]
    dividendRate: Optional[float]
    regularMarketPreviousClose: Optional[float]

    bid: Optional[float]
    ask: Optional[float]
    bidSize: Optional[int]
    askSize: Optional[int]

    fullExchangeName: Optional[str]
    financialCurrency: Optional[str]
    regularMarketOpen: Optional[float]

    averageDailyVolume3Month: Optional[int]
    averageDailyVolume10Day: Optional[int]

    fiftyTwoWeekLowChange: Optional[float]
    fiftyTwoWeekLowChangePercent: Optional[float]
    firstTradeDateMilliseconds: Optional[int]

    regularMarketChange: Optional[float]
    regularMarketTime: Optional[int]
    regularMarketDayHigh: Optional[float]
    regularMarketDayRange: Optional[str]

    trailingAnnualDividendYield: Optional[float]
    dividendYield: Optional[float]

    epsTrailingTwelveMonths: Optional[float]
    epsForward: Optional[float]
    epsCurrentYear: Optional[float]
    priceEpsCurrentYear: Optional[float]

    sharesOutstanding: Optional[int]
    bookValue: Optional[float]

    fiftyDayAverage: Optional[float]
    fiftyDayAverageChange: Optional[float]
    fiftyDayAverageChangePercent: Optional[float]

    twoHundredDayAverage: Optional[float]
    twoHundredDayAverageChange: Optional[float]
    twoHundredDayAverageChangePercent: Optional[float]

    marketCap: Optional[int]
    forwardPE: Optional[float]
    priceToBook: Optional[float]

    sourceInterval: Optional[int]
    exchangeDataDelayedBy: Optional[int]

    averageAnalystRating: Optional[str]

    tradeable: Optional[bool]
    cryptoTradeable: Optional[bool]
    priceHint: Optional[int]

    displayName: Optional[str]
    symbol: str


class Meta(BaseModel):
    version: str
    status: int
    copywrite: str
    symbol: str
    processedTime: datetime


class StockQuotes(BaseModel):
    meta: Meta
    body: List[Quote]

    @field_validator('body', mode='before')
    @classmethod
    def skip_invalid_items(cls, value):
        valid_items = []
        for i, item in enumerate(value):
            try:
                valid_items.append(Quote(**item))
            except ValidationError:
                log_title = 'mboum json map error'
                log_message = 'mboum_quote_schema, json:{}'

                utils.output_to_logfile(
                    log_type=OutputLogType.apilog,
                    title=log_title,
                    log_message=log_message.format(item))
        return valid_items
