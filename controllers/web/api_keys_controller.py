from flask import Blueprint, request

from system.database import DatabaseSession
from services.api_key_service import api_key_service
from schemas.api_key_schema import ApiKeyAdd
from services.auth_service import auth_service
from system.exceptions import EFAuthException
from utilities.utils import utils

api_keys_bp = Blueprint('api_keys_bp', __name__)


@api_keys_bp.route('', methods=['GET'])
def list_keys():
    with DatabaseSession() as db:
        user_auth = auth_service.is_valid_signin(db, request.headers)
        if user_auth is None:
            raise EFAuthException('Unauthorized access.')

        keys = api_key_service.list_all(db)
        return utils.ok([k.model_dump() for k in keys])


@api_keys_bp.route('', methods=['POST'])
def create_key():
    data = request.get_json(force=True)
    dto = ApiKeyAdd(**data)

    with DatabaseSession() as db:
        user_auth = auth_service.is_valid_signin(db, request.headers)
        if user_auth is None:
            raise EFAuthException('Unauthorized access.')

        key_view = api_key_service.add(db, dto)
        return utils.ok(key_view.model_dump())


@api_keys_bp.route('/<int:api_key_id>/activate', methods=['POST'])
def activate_key(api_key_id: int):
    with DatabaseSession() as db:
        user_auth = auth_service.is_valid_signin(db, request.headers)
        if user_auth is None:
            raise EFAuthException('Unauthorized access.')

        if api_key_service.set_active(db, api_key_id, True) is False:
            return utils.ok({'updated': False}, 404)
        return utils.ok({'updated': True})


@api_keys_bp.route('/<int:api_key_id>/deactivate', methods=['POST'])
def deactivate_key(api_key_id: int):
    with DatabaseSession() as db:
        user_auth = auth_service.is_valid_signin(db, request.headers)
        if user_auth is None:
            raise EFAuthException('Unauthorized access.')

        if api_key_service.set_active(db, api_key_id, False) is False:
            return utils.ok({'updated': False}, 404)
        return utils.ok({'updated': True})


@api_keys_bp.route('/<int:api_key_id>', methods=['DELETE'])
def delete_key(api_key_id: int):
    with DatabaseSession() as db:
        user_auth = auth_service.is_valid_signin(db, request.headers)
        if user_auth is None:
            raise EFAuthException('Unauthorized access.')

        if api_key_service.delete(db, api_key_id) is False:
            return utils.ok({'deleted': False}, 404)
        return utils.ok({'deleted': True})
