from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Meta(BaseModel):
    symbol: str
    expiration: Optional[int]
    processedTime: datetime
    version: str
    status: int
    copywrite: str


class OptionContract(BaseModel):
    contractSymbol: Optional[str]
    strike: Optional[float]
    currency: Optional[str]
    lastPrice: Optional[float]
    change: Optional[float]
    percentChange: Optional[float]
    volume: Optional[int]
    openInterest: Optional[int]
    bid: Optional[float]
    ask: Optional[float]
    contractSize: Optional[str]
    expiration: Optional[int]
    lastTradeDate: Optional[int]
    impliedVolatility: Optional[float]
    inTheMoney: Optional[bool]


class OptionChain(BaseModel):
    expirationDate: Optional[int]
    hasMiniOptions: Optional[bool]
    calls: Optional[List[OptionContract]]
    puts: Optional[List[OptionContract]]


class Quote(BaseModel):
    language: Optional[str]
    region: Optional[str]
    quoteType: Optional[str]
    typeDisp: Optional[str]
    quoteSourceName: Optional[str]
    triggerable: Optional[bool]
    customPriceAlertConfidence: Optional[str]
    currency: Optional[str]
    marketState: Optional[str]
    regularMarketChangePercent: Optional[float]
    regularMarketPrice: Optional[float]
    exchange: Optional[str]
    shortName: Optional[str]
    longName: Optional[str]
    messageBoardId: Optional[str]
    exchangeTimezoneName: Optional[str]
    exchangeTimezoneShortName: Optional[str]
    gmtOffSetMilliseconds: Optional[int]
    market: Optional[str]
    esgPopulated: Optional[bool]
    firstTradeDateMilliseconds: Optional[int]
    sharesOutstanding: Optional[int]
    bookValue: Optional[float]
    fiftyDayAverage: Optional[float]
    fiftyDayAverageChange: Optional[float]
    fiftyDayAverageChangePercent: Optional[float]
    twoHundredDayAverage: Optional[float]
    twoHundredDayAverageChange: Optional[float]
    marketCap: Optional[int]
    forwardPE: Optional[float]
    priceToBook: Optional[float]
    sourceInterval: Optional[int]
    exchangeDataDelayedBy: Optional[int]
    averageAnalystRating: Optional[str]
    tradeable: Optional[bool]
    cryptoTradeable: Optional[bool]
    priceHint: Optional[int]
    postMarketChangePercent: Optional[float]
    postMarketTime: Optional[int]
    postMarketPrice: Optional[float]
    postMarketChange: Optional[float]
    regularMarketChange: Optional[float]
    regularMarketTime: Optional[int]
    regularMarketDayHigh: Optional[float]
    regularMarketDayRange: Optional[str]
    regularMarketDayLow: Optional[float]
    regularMarketVolume: Optional[int]
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
    trailingAnnualDividendYield: Optional[float]
    dividendYield: Optional[float]
    epsTrailingTwelveMonths: Optional[float]
    epsForward: Optional[float]
    epsCurrentYear: Optional[float]
    priceEpsCurrentYear: Optional[float]
    twoHundredDayAverageChangePercent: Optional[float]
    displayName: Optional[str]
    symbol: Optional[str]


class OptionData(BaseModel):
    underlyingSymbol: Optional[str]
    expirationDates: Optional[List[int]]
    strikes: Optional[List[float]]
    hasMiniOptions: Optional[bool]
    quote: Optional[Quote]
    options: Optional[List[OptionChain]]


class OptionPrices(BaseModel):
    meta: Meta
    body: List[OptionData]
