from flask import Blueprint, request

from utilities.utils import utils
from system.database import DatabaseSession
from services.api_key_service import api_key_service
from system.exceptions import EFAuthException

companies_bp = Blueprint('companies_bp', __name__)


@companies_bp.before_request
def authenticate():
    with DatabaseSession() as db:
        api_key = utils.get_api_key_from_header(request.headers)
        if not api_key:
            raise EFAuthException('API key required.')
        model = api_key_service.get_active_by_value(db, api_key)
        if model is None:
            raise EFAuthException('Invalid API key.')
        api_key_service.touch_last_used(db, model)


@companies_bp.route('/test', methods=['POST'])
def test():

    return utils.ok({})
