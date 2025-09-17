from datetime import date
from sqlalchemy.orm import Session

from models.market_holiday_model import MarketHolidayModel


class market_holiday_service:

    @staticmethod
    def get_holiday_close(db: Session, check_date: date) -> MarketHolidayModel | None:
        result = db.query(MarketHolidayModel).filter(MarketHolidayModel.holiday_date == check_date).first()

        return result
