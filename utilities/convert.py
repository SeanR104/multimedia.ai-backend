import pytz
import time
from decimal import Decimal
from datetime import datetime, date
from dateutil import parser

from utilities.constants import OptionType

from system.exceptions import EFBadRequestException


class convert:

    @staticmethod
    def string_to_float(value: str, default_value: float = 0) -> float:
        if len(value) == 0:
            return default_value

        value = value.replace('(', '')
        value = value.replace(')', '')
        value = value.replace('\"', '')
        value = value.replace('$', '')
        value = value.replace(',', '')

        return float(value)

    @staticmethod
    def to_timezone(value, target_timezone: str) -> datetime:
        if type(value) is str:
            date_value = parser.parse(value)
        else:
            date_value = value

        date_value = date_value.astimezone(pytz.timezone(target_timezone))

        return date_value

    @staticmethod
    def epoch_to_utc(timestamp: int) -> datetime:
        date_time = datetime.fromtimestamp(timestamp)

        system_timezone = datetime.now().astimezone().tzinfo
        if str(system_timezone) == 'EDT' or str(system_timezone) == 'EST':
            date_time = date_time.astimezone(pytz.timezone('America/New_York'))
            date_time = date_time.astimezone(pytz.timezone('UTC'))
        if str(system_timezone) == 'CDT' or str(system_timezone) == 'CST':
            date_time = date_time.astimezone(pytz.timezone('America/Chicago'))
            date_time = date_time.astimezone(pytz.timezone('UTC'))

        return date_time

    @staticmethod
    def utc_to_epoch(date_time: datetime) -> int:
        system_timezone = datetime.now().astimezone().tzinfo
        if str(system_timezone) == 'EDT' or str(system_timezone) == 'EST':
            date_time = date_time.astimezone(pytz.timezone('America/New_York'))
        if str(system_timezone) == 'CDT' or str(system_timezone) == 'CST':
            date_time = date_time.astimezone(pytz.timezone('America/Chicago'))

        return int(time.mktime(date_time.timetuple()))

    @staticmethod
    def option_underlying(value) -> float:
        if type(value) is str or type(value) is Decimal or type(value) is int:
            value = float(value)
        if type(value) is float:
            return round(value, 0)
        raise Exception('Option underlying type conversion error.')

    @staticmethod
    def option_strike(price) -> float:
        if type(price) is str or type(price) is Decimal or type(price) is int:
            price = float(price)
        if type(price) is float:
            return round(price, 4)
        raise Exception('Option strike type conversion error.')

    @staticmethod
    def option_expiration(value) -> date:
        if type(value) is str:
            value = parser.parse(value).date()
        if type(value) is datetime:
            value = value.date()
        if type(value) is date:
            return value
        raise Exception('Option expiration type conversion error.')

    @staticmethod
    def trade_quantity(quantity) -> float:
        if type(quantity) is str or type(quantity) is Decimal or type(quantity) is int:
            quantity = float(quantity)
        if type(quantity) is float:
            return round(quantity, 5)
        raise Exception('Trade quantity type conversion error.')

    @staticmethod
    def trade_contracts(contracts) -> float:
        if type(contracts) is str or type(contracts) is Decimal or type(contracts) is int:
            contracts = float(contracts)
        if type(contracts) is float:
            return round(contracts, 0)
        raise Exception('Trade contracts type conversion error.')

    @staticmethod
    def trade_date(value) -> date:
        if type(value) is str:
            value = parser.parse(value).date()
        if type(value) is datetime:
            value = value.date()
        if type(value) is date:
            return value
        raise Exception('Trade date type conversion error.')

    @staticmethod
    def trade_price(price) -> float:
        if type(price) is str or type(price) is Decimal or type(price) is int:
            price = float(price)
        if type(price) is float:
            return round(price, 5)
        raise Exception('Trade price type conversion error.')

    @staticmethod
    def trade_commission(commission) -> float:
        if type(commission) is str or type(commission) is Decimal or type(commission) is int:
            commission = float(commission)
        if type(commission) is float:
            return round(commission, 4)
        raise Exception('Trade commission type conversion error.')

    @staticmethod
    def special_dividend(dividend) -> float:
        if type(dividend) is str or type(dividend) is Decimal or type(dividend) is int:
            dividend = float(dividend)
        if type(dividend) is float:
            return round(dividend, 4)
        raise Exception('Special dividend type conversion error.')

    @staticmethod
    def split_ratio(ratio) -> float:
        if type(ratio) is str or type(ratio) is Decimal or type(ratio) is int:
            ratio = float(ratio)
        if type(ratio) is float:
            return round(ratio, 5)
        raise Exception('Split ratio type conversion error.')

    @staticmethod
    def dollar_decimal(dollar) -> float:
        if type(dollar) is str or type(dollar) is Decimal or type(dollar) is int:
            dollar = float(dollar)
        if type(dollar) is float:
            return round(dollar, 2)
        raise Exception('Dollar value type conversion error.')

    @staticmethod
    def dollar_precise(dollar) -> float:
        if type(dollar) is str or type(dollar) is Decimal or type(dollar) is int:
            dollar = float(dollar)
        if type(dollar) is float:
            return round(dollar, 4)
        raise Exception('Dollar precise value type conversion error.')

    @staticmethod
    def percentage_decimal(percent) -> float:
        if type(percent) is str or type(percent) is Decimal or type(percent) is int:
            percent = float(percent)
        if type(percent) is float:
            return round(percent, 4)
        raise Exception('Percentage value type conversion error.')

    @staticmethod
    def percent_change(previous_value, current_value) -> float:
        previous_value = convert.dollar_precise(previous_value)
        current_value = convert.dollar_precise(current_value)

        if previous_value == 0:
            return 0.0

        change_percent = ((current_value / previous_value) - 1) * 100
        change_percent = convert.percentage_decimal(change_percent)

        return change_percent

    @staticmethod
    def mid_price(bid_price, ask_price) -> float:
        bid_price = convert.dollar_precise(bid_price)
        ask_price = convert.dollar_precise(ask_price)

        mid_price = (bid_price + ask_price) / 2

        return round(mid_price, 5)

    @staticmethod
    def set_trade_numerical_sign(transaction_sign: int, amount):
        amount = convert.dollar_precise(amount)
        amount = abs(amount)

        trade_amount = convert.dollar_decimal(amount * transaction_sign)
        return trade_amount

    @staticmethod
    def percent_text(number, precision, include_sign: bool = False) -> str:
        if number is None:
            return ''

        number = convert.dollar_precise(number)
        number = round(number, precision)

        return_text = '{0:,.{1}f}'.format(number, precision) + '%'

        if include_sign is True:
            is_positive = True if number > 0 else False
            return_text = ('+' if is_positive is True else '') + return_text

        return return_text

    @staticmethod
    def number_text(number, precision, trailing_zeros: bool = False, truncate: bool = False, include_sign: bool = False) -> str:
        return_text = ''

        if number is None:
            return return_text

        if truncate is True:
            if number > 999999999999:
                precision = -10
            elif number > 999999999:
                precision = -7
            elif number > 999999:
                precision = -4
            elif number > 999:
                precision = -1

        number = round(float(number), precision)
        if precision > 0:
            return_text = '{0:,.{1}f}'.format(number, precision)
        else:
            return_text = '{0:,.0f}'.format(number)

        has_decimal = True if return_text.find('.') > -1 else False

        if trailing_zeros is False and has_decimal is True:
            return_text = return_text.rstrip('0').rstrip('.')

        if truncate is True:
            thousands = return_text.count(',')
            if thousands > 0:
                i = return_text.find(',')
                return_text = return_text[0: i + 3]
                return_text = return_text.replace(',', '.')

                if thousands == 1:
                    return_text += 'K'
                elif thousands == 2:
                    return_text += 'M'
                elif thousands == 3:
                    return_text += 'B'
                elif thousands == 4:
                    return_text += "T"

        if include_sign is True:
            is_positive = True if number > 0 else False
            return_text = ('+' if is_positive is True else '') + return_text

        return return_text

    @staticmethod
    def money_text(money) -> str:
        if money is None:
            return ''
        
        money = round(money, 2)

        return '$' + '{0:,.2f}'.format(money)

    @staticmethod
    def datetime_text(date_val: datetime, include_day_of_week: bool) -> str:
        if date_val is None:
            return ''

        if include_day_of_week is True:
            date_val = date_val.strftime('%a. %b %d, %Y')
        else:
            date_val = date_val.strftime('%b %d, %Y')

        return date_val

    @staticmethod
    def option_text_pretty(ticker_symbol: str, expiration_date: date, option_type: str, strike_price: float) -> str:
        option_ticker = '{} {} ${} {}'
        exp_date_text = expiration_date.strftime('%Y-%m-%d')
        option_type_letter = 'C' if option_type == OptionType.call else 'P'

        price_text = '{0:.2f}'.format(strike_price)
        decimal_pos = price_text.find('.')
        decimal_precision = len(price_text) - decimal_pos

        if decimal_precision > 4:
            message = 'Option strike price has too many decimal places, {} {} {} {}'
            message = message.format(ticker_symbol, str(expiration_date), option_type, str(strike_price))
            raise EFBadRequestException(message)
        if decimal_pos > 5:
            message = 'Option strike price is too large, {} {} {} {}'
            message = message.format(ticker_symbol, str(expiration_date), option_type, str(strike_price))
            raise EFBadRequestException(message)

        option_ticker = option_ticker.format(ticker_symbol, exp_date_text, price_text, option_type_letter)

        return option_ticker

    @staticmethod
    def option_ticker(ticker_symbol: str, expiration_date: date, option_type: str, strike_price: float) -> str:
        ticker_value = '{}{}{}{}'
        exp_date_text = expiration_date.strftime('%y%m%d')
        option_type_letter = 'C' if option_type == OptionType.call else 'P'

        price_text = str(strike_price)
        decimal_pos = price_text.find('.')
        decimal_precision = len(price_text) - decimal_pos

        if decimal_precision > 4:
            message = 'Option strike price has too many decimal places, {} {} {} {}'
            message = message.format(ticker_symbol, str(expiration_date), option_type, str(strike_price))
            raise EFBadRequestException(message)
        if decimal_pos > 5:
            message = 'Option strike price is too large, {} {} {} {}'
            message = message.format(ticker_symbol, str(expiration_date), option_type, str(strike_price))
            raise EFBadRequestException(message)

        # pad the zeros, ex: $123.45 = 00123450
        if decimal_pos == -1:
            price_text += '000'
        elif decimal_precision == 2:
            price_text += '00'
        elif decimal_precision == 3:
            price_text += '0'
        for x in range(decimal_pos, 5):
            price_text = '0' + price_text
        price_text = price_text.replace('.', '')

        ticker_symbol = ticker_symbol.replace('.', '').replace('-', '')

        ticker_value = ticker_value.format(ticker_symbol, exp_date_text, option_type_letter, price_text)

        return ticker_value
