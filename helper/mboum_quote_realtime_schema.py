from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class KeyValueLabel(BaseModel):
    label: Optional[str]
    value: Optional[str]


class KeyStats(BaseModel):
    fiftyTwoWeekHighLow: KeyValueLabel
    dayrange: KeyValueLabel


class TradeData(BaseModel):
    lastSalePrice: Optional[str]
    netChange: Optional[str]
    percentageChange: Optional[str]
    deltaIndicator: Optional[str]
    lastTradeTimestamp: Optional[str]
    isRealTime: Optional[bool]
    bidPrice: Optional[str]
    askPrice: Optional[str]
    bidSize: Optional[str]
    askSize: Optional[str]
    volume: Optional[str]


class Body(BaseModel):
    symbol: Optional[str]
    companyName: Optional[str]
    stockType: Optional[str]
    exchange: Optional[str]
    primaryData: TradeData
    secondaryData: TradeData
    marketStatus: Optional[str]
    assetClass: Optional[str]
    keyStats: KeyStats


class Meta(BaseModel):
    version: Optional[str]
    status: Optional[int]
    copywrite: Optional[str]
    processedTime: Optional[datetime]


class StockQuoteRealTime(BaseModel):
    meta: Meta
    body: Body
