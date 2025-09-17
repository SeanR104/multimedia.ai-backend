from flask import Blueprint, request

from schemas.user_schema import UserAdd
from services.user_service import user_service
from system.database import DatabaseSession
from utilities.utils import utils
users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    data['user_role_type'] = 'user'
    user_create = UserAdd(**data)
    with DatabaseSession() as db:
        user_service.create(db, user_create)

    return utils.ok()
