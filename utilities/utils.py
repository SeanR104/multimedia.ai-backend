import json
import bcrypt
import pytz
import traceback
import datetime
import logging
from flask import Response, current_app
from decimal import Decimal
from dateutil import tz, parser
from dateutil.relativedelta import relativedelta

from utilities.convert import convert
from utilities.constants import OutputLogType

from system.exceptions import EFBadRequestException, EFServerException


class utils:
    @staticmethod
    def check_password(password_text: str, password_hash: str) -> bool:
        password_encoded = password_text.encode('UTF-8')
        hash_encoded = password_hash.encode('UTF-8')

        if bcrypt.checkpw(password_encoded, hash_encoded) is True:
            return True

        return False

    @staticmethod
    def get_token_from_header(http_header: dict) -> str:
        token = ''
        auth = 'authorization'
        for key in http_header.keys():
            if auth == key.lower():
                token = http_header[key].split(' ')
                if len(token) > 1 and token[0] == 'Bearer':
                    token = token[1]
                break
        return token

    @staticmethod
    def get_api_key_from_header(http_header: dict) -> str:
        # Supports either X-API-Key: <key> or Authorization: ApiKey <key>
        # Returns empty string if not found
        for key, value in http_header.items():
            k = key.lower()
            if k == 'x-api-key':
                return value.strip()
            if k == 'authorization':
                parts = str(value).split(' ')
                if len(parts) > 1 and parts[0] in ('ApiKey', 'Api-Key', 'Api_Key'):
                    return parts[1].strip()
        return ''

    @staticmethod
    def ok(json_value: object = None, status_code: int = 200):
        if json_value is None:
            return '', status_code
        json_string = json.dumps(json_value, default=utils.json_serial)
        return Response(json_string, mimetype='application/json'), status_code

    @staticmethod
    def json_serial(obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return round(float(obj), 2)
        raise EFServerException("Type %s not serializable" % type(obj))

    @staticmethod
    def output_to_logfile(log_type: str, title: str = None, log_message: str = None, exception: Exception = None, trace: str = None):
        etz_now = utils.get_easterntime_now()

        logger = logging.getLogger(current_app.config['APP_NAME'])

        log_entry = {
            'app_name': current_app.config['APP_NAME'],
            'time_tag': str(etz_now),
            'title': title,
            'log_message': log_message}

        if exception is not None:
            log_entry['exception_type'] = str(type(exception))
            log_entry['exception_message'] = str(exception).partition('\n')[0]
        else:
            log_entry['exception_type'] = ""
            log_entry['exception_message'] = ""

        log_entry['trace'] = trace

        try:
            if log_type == OutputLogType.infolog:
                logger.info(json.dumps(log_entry))
            else:
                logger.error(json.dumps(log_entry))

        except Exception as ex:
            exception_log = 'EXCEPTION:: failed to log to file.\nException: {}\nStack Trace: {}'
            exception_message = str(type(ex)) + '\n'
            exception_message += str(ex).partition('\n')[0]
            logger.critical(exception_log.format(exception_message, traceback.format_exc()))
            logger.critical(json.dumps(log_entry))

        return

    @staticmethod
    def get_easterntime_now() -> datetime.datetime:
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        etz_now = utc_now.astimezone(pytz.timezone('America/New_York'))

        return etz_now

    @staticmethod
    def null_date_value() -> datetime.date:
        return datetime.date(1, 1, 1)

    @staticmethod
    def is_date_null(date_value: datetime.date) -> bool:
        if date_value == utils.null_date_value():
            return True
        return False

    @staticmethod
    def null_datetime_value() -> datetime.datetime:
        return datetime.datetime(1, 1, 1, 0, 0, 0)

    @staticmethod
    def is_datetime_null(date_value: datetime.datetime) -> bool:
        if date_value == utils.null_datetime_value():
            return True
        return False

    @staticmethod
    def null_time_value() -> datetime.time:
        return datetime.time(1, 1, 1, 111, tzinfo=tz.tzoffset('UTC-1', -1))

    @staticmethod
    def is_time_null(time_value: datetime.time) -> bool:
        if time_value == utils.null_time_value():
            return True
        return False

    @staticmethod
    def generate_password_hash(password) -> str:
        password_encoded = password.encode('UTF-8')

        salt = bcrypt.gensalt(rounds=12)
        hash_value = bcrypt.hashpw(password_encoded, salt)

        password_hash = hash_value.decode()

        return password_hash

    @staticmethod
    def order_for_tax_advantage(close_trade: dict, open_list: list[dict]):
        # 1) sell short-term loss
        # 2) sell long-term loss
        # >>> from the greatest loss to smallest
        # 3) sell long-term gain
        # 4) sell short-term gain
        # >>> from the smallest gain to largest

        one_year_ago = close_trade['trade_date'] - relativedelta(years=1) - relativedelta(days=1)

        short_losses = [b for b in open_list if
                        b['trade_date'] > one_year_ago and
                        convert.trade_price(b['trade_price']) > convert.trade_price(close_trade['trade_price'])]
        long_losses = [b for b in open_list if
                       b['trade_date'] <= one_year_ago and
                       convert.trade_price(b['trade_price']) > convert.trade_price(close_trade['trade_price'])]
        long_gains = [b for b in open_list if
                      b['trade_date'] <= one_year_ago and
                      convert.trade_price(b['trade_price']) <= convert.trade_price(close_trade['trade_price'])]
        short_gains = [b for b in open_list if
                       b['trade_date'] > one_year_ago and
                       convert.trade_price(b['trade_price']) <= convert.trade_price(close_trade['trade_price'])]

        return_list = []

        if len(short_losses) > 0:
            return_list += sorted(short_losses, key=lambda s: s['trade_price'], reverse=True)
        if len(long_losses) > 0:
            return_list += sorted(long_losses, key=lambda s: s['trade_price'], reverse=True)
        if len(long_gains) > 0:
            return_list += sorted(long_gains, key=lambda s: s['trade_price'], reverse=True)
        if len(short_gains) > 0:
            return_list += sorted(short_gains, key=lambda s: s['trade_price'], reverse=True)

        return return_list

    @staticmethod
    def order_for_fifo(open_list: list[dict]):
        # The newest transaction is closed first

        open_list.sort(key=lambda s: s['trade_date'], reverse=True)

        return open_list

    @staticmethod
    def order_for_lifo(open_list: list[dict]):
        # The oldest transaction is closed first

        open_list.sort(key=lambda s: s['trade_date'], reverse=False)

        return open_list

    @staticmethod
    def calculate_trade_amount_option(transaction_sign: int, contracts, price, commission, underlying_shares):
        contracts = convert.trade_contracts(contracts)
        contracts = abs(contracts)

        price = convert.trade_price(price)
        price = abs(price)

        commission = convert.trade_commission(commission)
        commission = abs(commission)

        underlying_shares = convert.option_underlying(underlying_shares)

        try:
            trade_amount = (contracts * price * underlying_shares * transaction_sign) - commission
        except Exception:
            raise EFServerException('Error calculating option trade amount.')

        trade_amount = convert.dollar_decimal(trade_amount)
        return trade_amount

    @staticmethod
    def calculate_trade_amount_stock(transaction_sign: int, quantity, price, commission):
        quantity = convert.trade_quantity(quantity)
        quantity = abs(quantity)

        price = convert.trade_price(price)
        price = abs(price)

        commission = convert.trade_commission(commission)
        commission = abs(commission)

        try:
            trade_amount = (quantity * price * transaction_sign) - commission
        except Exception:
            raise EFServerException('Error calculating stock trade amount.')

        trade_amount = convert.dollar_decimal(trade_amount)
        return trade_amount
