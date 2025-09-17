from flask import Blueprint, request
from datetime import datetime

from services.market_holiday_service import market_holiday_service
from system.database import DatabaseSession
from services.api_key_service import api_key_service
from system.exceptions import EFAuthException

from utilities.utils import utils

markets_bp = Blueprint('markets_bp', __name__)


@markets_bp.before_request
def authenticate():
    with DatabaseSession() as db:
        api_key = utils.get_api_key_from_header(request.headers)
        if not api_key:
            raise EFAuthException('API key required.')
        model = api_key_service.get_active_by_value(db, api_key)
        if model is None:
            raise EFAuthException('Invalid API key.')
        api_key_service.touch_last_used(db, model)


@markets_bp.route('/is_open', methods=['GET'])
def is_open():
    market_open = False

    etz_now = utils.get_easterntime_now()
    market_open_etz = etz_now.replace(hour=9, minute=30, second=-0, microsecond=0)
    market_close_etz = etz_now.replace(hour=16, minute=0, second=0, microsecond=0)

    with DatabaseSession() as db:
        today_holiday = market_holiday_service.get_holiday_close(db, etz_now.date())

    is_weekday = True if etz_now.date().isoweekday() < 6 else False
    if is_weekday is True:
        market_close_etz_time = market_close_etz.time()

        if today_holiday is not None:
            market_close_etz_time = today_holiday.close_local_tz

        if market_open_etz.time() <= etz_now.time() <= market_close_etz_time:
            market_open = True

    dto = {
        'market_open': market_open,
    }

    return utils.ok(dto)


@markets_bp.route('/close_etz', methods=['GET'])
def close_etz():
    market_date = request.args.get('market_date')
    market_date = datetime.strptime(market_date, "%Y-%m-%d")

    market_date_close_time = market_date.replace(hour=16, minute=0, second=0, microsecond=0)

    with DatabaseSession() as db:
        market_holiday = market_holiday_service.get_holiday_close(db, market_date.date())

    if market_holiday is not None:
        close_time = market_holiday.close_local_tz

        market_date_close_time = market_date_close_time.replace(
            hour=close_time.hour,
            minute=close_time.minute,
            second=0,
            microsecond=0)

    dto = {
        'close_time': market_date_close_time,
    }

    return utils.ok(dto)
