import traceback
from datetime import datetime

from flask import current_app

from helper.mboum_api_helper import mboum_api_helper
from helper.mboum_option_schema import Quote
from helper.mboum_quote_schema import StockQuotes
from schemas.company_detail_schema import CompanyDetailSchema
from schemas.company_earning_schema import CompanyEarningSchema
from schemas.price_equity_schema import PriceEquitySchema
from schemas.stock_ticker_schema import StockTickerSchema
from utilities.constants import OutputLogType
from utilities.convert import convert
from utilities.utils import utils

PLATFORM_NAME = 'stock-lookup'


class api_stocks_helper:
    @staticmethod
    def mboum_get_price(request_symbols: list[str]) -> list[dict]:
        api_base_url = current_app.config['STOCKS_API_BASE_URL']

        quote_url = '{}markets/stock/quotes/'.format(api_base_url)

        return_list = []

        if len(request_symbols) == 0:
            return return_list

        symbols_lookup_string = ','.join(request_symbols)

        parameters = {
            'ticker': symbols_lookup_string
        }

        response_json = mboum_api_helper.make_api_request(PLATFORM_NAME, quote_url, parameters)
        if len(response_json) == 0:
            return return_list

        if "message" in response_json and response_json["message"] == "Invalid tickers":
            log_title = 'mboum api request failed'
            log_message = 'mboum_get_price, invalid tickers: {}'
            utils.output_to_logfile(OutputLogType.apilog, title=log_title, log_message=log_message.format(symbols_lookup_string))

            return []

        stock_quotes = StockQuotes(**response_json)
        # Compare requested vs returned symbols and log any not-found tickers
        stocks_requested = set(request_symbols)
        stocks_returned = set([q.symbol for q in stock_quotes.body]) if stock_quotes and stock_quotes.body else set()
        not_found = sorted(list(stocks_requested - stocks_returned))
        if len(not_found) > 0:
            utils.output_to_logfile(
                log_type=OutputLogType.apilog,
                title='mboum_get_price missing tickers',
                log_message=f'not_found={", ".join(not_found)} requested={len(request_symbols)} returned={len(stocks_returned)}'
            )

        if len(stock_quotes.body) > 0:
            for quote in stock_quotes.body:
                price, company = api_stocks_helper.__fill_props(quote)
                return_list.append((price, company))
        else:
            log_title = 'mboum api request body empty'
            log_message = 'mboum_get_price, tickers: {}'
            utils.output_to_logfile(OutputLogType.apilog, title=log_title, log_message=log_message.format(symbols_lookup_string))

        return return_list

    @staticmethod
    def __fill_props(quote: Quote) -> tuple[PriceEquitySchema, CompanyEarningSchema]:
        def to_dt(ts: int | None) -> datetime:
            return convert.epoch_to_utc(ts) if ts is not None else None

        company_detail = CompanyDetailSchema(
            short_name=quote.shortName if quote.shortName is not None else '',
            long_name=quote.longName if quote.longName is not None else '',
            cik_code='',
            locale_name=quote.market if quote.market is not None else '',
            primary_exchange=quote.fullExchangeName if quote.fullExchangeName is not None else '',
            currency_type=quote.currency if quote.currency is not None else '',
            stock_type=quote.quoteType if quote.quoteType is not None else '',
            company_profile='',
            num_employees=0,
            company_sector='',
            company_industry='',
            company_address1='',
            company_address2='',
            company_city='',
            company_state='',
            company_zip='',
            company_country='',
            company_website='',
            company_phone='',
        )

        stock_ticker = StockTickerSchema(
            ticker_symbol=quote.symbol,
            stock_ticker_active=True,
            last_updated_profile=None,
            start_use_date=None,
            end_use_date=None,
            company_detail=company_detail,
        )

        # Use explicit None checks instead of truthy fallbacks for clarity
        price_equity = PriceEquitySchema(
            last_trade_price=quote.regularMarketPrice if quote.regularMarketPrice is not None else -1.0,
            bid_price=quote.bid if quote.bid is not None else -1.0,
            bid_size=quote.bidSize if quote.bidSize is not None else -1.0,
            ask_price=quote.ask if quote.ask is not None else -1.0,
            ask_size=quote.askSize if quote.askSize is not None else -1.0,
            day_high_price=quote.regularMarketDayHigh if quote.regularMarketDayHigh is not None else -1.0,
            day_low_price=quote.regularMarketDayLow if quote.regularMarketDayLow is not None else -1.0,
            fiftytwo_week_high=quote.fiftyTwoWeekHigh if quote.fiftyTwoWeekHigh is not None else -1.0,
            fiftytwo_week_low=quote.fiftyTwoWeekLow if quote.fiftyTwoWeekLow is not None else -1.0,
            previous_close=quote.regularMarketPreviousClose if quote.regularMarketPreviousClose is not None else -1.0,
            last_tradeutc=to_dt(quote.regularMarketTime),
            post_market_price=quote.postMarketPrice if quote.postMarketPrice is not None else -1.0,
            post_market_tradeutc=to_dt(quote.postMarketTime),
            stock_ticker=stock_ticker,
        )

        company_earning = CompanyEarningSchema(
            book_value=quote.bookValue if quote.bookValue is not None else -1.0,
            eps_forward=quote.epsForward if quote.epsForward is not None else -1.0,
            eps_trailing=quote.epsTrailingTwelveMonths if quote.epsTrailingTwelveMonths is not None else -1.0,
            dividend_rate_trailing=quote.trailingAnnualDividendRate if quote.trailingAnnualDividendRate is not None else -1.0,
            dividend_date=to_dt(quote.dividendDate),
            earnings_date_last=to_dt(quote.earningsTimestamp),
            earnings_date_next_start=to_dt(quote.earningsTimestampStart),
            earnings_date_next_end=to_dt(quote.earningsTimestampEnd),
            market_cap=quote.marketCap if quote.marketCap is not None else -1.0,
            shares_outstanding=quote.sharesOutstanding if quote.sharesOutstanding is not None else -1.0,
            day_volume=quote.regularMarketVolume if quote.regularMarketVolume is not None else -1.0,
            day_volume_average_10_days=quote.averageDailyVolume10Day if quote.averageDailyVolume10Day is not None else -1.0,
            day_volume_average_3_months=quote.averageDailyVolume3Month if quote.averageDailyVolume3Month is not None else -1.0,
            stock_ticker=stock_ticker,
        )

        if company_detail.short_name == '' and company_detail.long_name != '':
            company_detail.short_name = company_detail.long_name
        elif company_detail.long_name == '' and company_detail.short_name != '':
            company_detail.long_name = company_detail.short_name

        return price_equity, company_earning

    @staticmethod
    def __find_valid_symbol(url_text: str, url_parameters: dict) -> str:
        tickers = url_parameters['ticker']
        ticker_list = tickers.split(",")

        def find_valid_subset(start, end):
            if start > end:
                return []

            subset = ",".join(ticker_list[start:end + 1])

            ## call mboum api
            parameters = {
                'ticker': subset
            }
            response_json = mboum_api_helper.make_api_request(PLATFORM_NAME, url_text, parameters)
            if "body" in response_json:
                return [subset]

            # if start == end:
            #     with DBConnect(auto_commit=True, read_only=False) as db:
            #         stock_ticker_service.deactivate(db, subset)
            #     return []

            mid = (start + end) // 2
            left_valid = find_valid_subset(start, mid)
            right_valid = find_valid_subset(mid + 1, end)

            return left_valid + right_valid

        valid_parts = find_valid_subset(0, len(ticker_list) - 1)

        return ",".join(valid_parts)

