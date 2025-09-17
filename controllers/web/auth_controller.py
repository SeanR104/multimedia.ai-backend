from flask import Blueprint, request

from schemas.auth_token_schema import AuthorizeUserDto
from system.database import DatabaseSession
from services.user_service import user_service
from services.auth_service import auth_service
from system.exceptions import EFBadRequestException, EFAuthException, EFServerException
from utilities.utils import utils

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/test', methods=['POST'])
def test():
    with DatabaseSession() as db:
        user_auth = auth_service.is_valid_signin(db, request.headers)
        if user_auth is None:
            raise EFAuthException('Unauthorized access.')

    raise EFServerException('Logging a test message.')


@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    auth_user = AuthorizeUserDto(**data)

    with DatabaseSession() as db:
        user = user_service.get_by_email_address(db, auth_user.email_address)
        if user is None:
            raise EFBadRequestException("Invalid email address or password.")

        if utils.check_password(auth_user.password, user.password_hash) is False:
            raise EFBadRequestException('Invalid email address or password.')

        auth_token = auth_service.generate_token(db, user.user_id)
        auth_service.clear_expired_tokens(db)

    # with read_db:
    #    accounts = user_account_service.get_by_user_id(read_db, user['user_id'])

        dto = {
            'user_uuid': user.user_uuid,
            'auth_token': auth_token,
        }

        return utils.ok(dto)
