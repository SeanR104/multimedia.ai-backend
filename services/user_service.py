from sqlalchemy.orm import Session
from schemas.user_schema import UserAdd
from models.user_model import UserModel
from utilities.utils import utils


class user_service:

    @staticmethod
    def get_by_email_address(db: Session, email_address: str) -> UserModel | None:
        user = db.query(UserModel).filter(UserModel.email_address == email_address).first()

        return user

    @staticmethod
    def create(db: Session, user: UserAdd):
        user_create = UserModel(**user.for_db(), password_hash=utils.generate_password_hash(user.new_password1))
        db.add(user_create)

        return
