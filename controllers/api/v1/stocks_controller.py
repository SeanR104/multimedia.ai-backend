from flask import Blueprint, request

from pydantic import ValidationError
from utilities.utils import utils
from system.exceptions import EFBadRequestException, EFAuthException
from utilities.constants import OutputLogType
from helper.api_stocks_helper import api_stocks_helper
from schemas.stocks_dto_schema import StockDto
from system.database import DatabaseSession
from services.api_key_service import api_key_service

stocks_bp = Blueprint('stocks_bp', __name__)


@stocks_bp.before_request
def authenticate():
    with DatabaseSession() as db:
        api_key = utils.get_api_key_from_header(request.headers)
        if not api_key:
            raise EFAuthException('API key required.')
        model = api_key_service.get_active_by_value(db, api_key)
        if model is None:
            raise EFAuthException('Invalid API key.')
        api_key_service.touch_last_used(db, model)


@stocks_bp.route('/update_from_list', methods=['POST'])
def update_from_list():
    data = request.get_json()
    if data is None:
        data = {}

    try:
        payload = StockDto(**data)
    except ValidationError as ve:
        # Only invalid when body is missing or stocks is not a list
        # TODO: this is not an appropriate message for Bad Request exceptions
        raise EFBadRequestException(f'Invalid request body: {ve.errors()}')

    stocks = payload.stocks

    # Proceed with valid stocks only; log if some were filtered out
    stocks_input = data.get('stocks')
    if stocks_input is None:
        original_count = 0
    else:
        original_count = len(stocks_input)
    valid_count = len(stocks)
    if valid_count < original_count:
        utils.output_to_logfile(
            log_type=OutputLogType.apilog,
            title='update_from_list input filtered',
            log_message=f'requested={original_count} valid={valid_count}'
        )

    dto = api_stocks_helper.mboum_get_price(stocks)

    return utils.ok(dto)
