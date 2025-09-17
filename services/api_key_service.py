import secrets
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.api_key_model import ApiKeyModel
from schemas.api_key_schema import ApiKeyAdd, ApiKeyView


class api_key_service:

    @staticmethod
    def generate_key() -> str:
        # 48 bytes -> 64 length urlsafe
        return secrets.token_urlsafe(48)

    @staticmethod
    def add(db: Session, dto: ApiKeyAdd) -> ApiKeyView:
        key = api_key_service.generate_key()
        model = ApiKeyModel(
            key_value=key,
            name=dto.name,
            is_active=True,
        )
        db.add(model)
        db.flush()
        return ApiKeyView(
            api_key_id=model.api_key_id,
            key_value=model.key_value,
            name=model.name,
            is_active=model.is_active,
            createdutc=model.createdutc,
            updatedutc=model.updatedutc,
            last_used_utc=model.last_used_utc,
            revokedutc=model.revokedutc,
        )

    @staticmethod
    def list_all(db: Session) -> List[ApiKeyView]:
        rows = db.execute(select(ApiKeyModel)).scalars().all()
        return [ApiKeyView(
            api_key_id=r.api_key_id,
            key_value=r.key_value,
            name=r.name,
            is_active=r.is_active,
            createdutc=r.createdutc,
            updatedutc=r.updatedutc,
            last_used_utc=r.last_used_utc,
            revokedutc=r.revokedutc,
        ) for r in rows]

    @staticmethod
    def get_by_id(db: Session, api_key_id: int) -> Optional[ApiKeyModel]:
        return db.get(ApiKeyModel, api_key_id)

    @staticmethod
    def get_active_by_value(db: Session, key_value: str) -> Optional[ApiKeyModel]:
        return (db.query(ApiKeyModel)
                .filter(ApiKeyModel.key_value == key_value)
                .filter(ApiKeyModel.is_active == True)
                .first())

    @staticmethod
    def set_active(db: Session, api_key_id: int, is_active: bool) -> bool:
        model = api_key_service.get_by_id(db, api_key_id)
        if model is None:
            return False
        model.is_active = is_active
        if not is_active:
            model.revokedutc = datetime.now(timezone.utc)
        return True

    @staticmethod
    def delete(db: Session, api_key_id: int) -> bool:
        model = api_key_service.get_by_id(db, api_key_id)
        if model is None:
            return False
        db.delete(model)
        return True

    @staticmethod
    def touch_last_used(db: Session, model: ApiKeyModel) -> None:
        model.last_used_utc = datetime.now(timezone.utc)
        return
