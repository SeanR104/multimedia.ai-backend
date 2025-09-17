import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.auth_token_schema import AuthTokenAdd
from schemas.view_schema import UserAuthSchema
from models.user_model import UserModel
from models.auth_token_model import AuthTokenModel
from utilities.utils import utils
from utilities.convert import convert

TOKEN_EXPIRATION_DAYS = 7


class auth_service:

    @staticmethod
    def is_valid_signin(db: Session, http_header) -> UserAuthSchema | None:
        token = utils.get_token_from_header(http_header)
        if len(token) == 0:
            return None

        model = auth_service.get_user_valid(db, token, check_is_admin=False)

        return model

    @staticmethod
    def get_user_valid(db: Session, auth_token: str, check_is_admin: bool) -> UserAuthSchema | None:
        sql = (
            select(
                UserModel.user_id,
                UserModel.user_uuid,
                UserModel.user_is_enabled,
                UserModel.user_role_type,
                AuthTokenModel.auth_token_expirationutc)
            .join(AuthTokenModel, AuthTokenModel.user_id == UserModel.user_id)
            .where(AuthTokenModel.auth_token == auth_token)
            .where(UserModel.user_is_deleted == False)
        )

        results = db.execute(sql).all()
        if results is None:
            return None

        models = []

        for row in results:
            mapping = dict(row._mapping)
            auth = UserAuthSchema(**mapping)
            models.append(auth)

        for auth in models:
            expirationutc = convert.to_timezone(auth.auth_token_expirationutc, 'UTC')

            if check_is_admin is True and auth.user_role_type != 'admin':
                return None

            utcnow = datetime.now(timezone.utc)
            if expirationutc < utcnow or auth.user_is_enabled is False:
                return None

            return auth

        return None

    @staticmethod
    def generate_token(db: Session, user_id: int) -> str:
        expiration = datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRATION_DAYS)
        token = str(uuid.uuid4())

        authtoken_add = AuthTokenAdd(
            user_id=user_id,
            auth_token=token,
            auth_token_expirationutc=expiration)

        authtoken_create = AuthTokenModel(**authtoken_add.model_dump())
        db.add(authtoken_create)

        return token

    @staticmethod
    def clear_expired_tokens(db: Session) -> None:
        utcnow = datetime.now(timezone.utc)

        (db.query(AuthTokenModel)
         .filter(AuthTokenModel.auth_token_expirationutc < utcnow)
         .delete(synchronize_session=False))

        return
