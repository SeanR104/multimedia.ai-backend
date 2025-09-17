import time
from flask import current_app

import requests
import traceback
from datetime import datetime, timezone

from models.search_api_status_model import SearchApiStatusModel
from models.search_api_history_model import SearchApiHistoryModel
from schemas.search_api_history_schema import SearchApiHistoryAdd
from schemas.search_api_status_schema import SearchApiStatusEdit, SearchApiStatusFilter
from system.database import DatabaseSession
from sqlalchemy.orm import Session
from utilities.utils import utils
from utilities.constants import OutputLogType

API_NAME = 'mboum'


class mboum_api_helper:

    @staticmethod
    def make_api_request(platform_name: str, url_text: str, url_parameters: dict) -> dict:
        status_code = 500

        with DatabaseSession() as db:
            status_edit = SearchApiStatusEdit(
                platform_running=platform_name)

            if mboum_api_helper.__get_lock_mboum_api(db, status_edit) is False:
                return {}

            last_runutc = mboum_api_helper.__get_last_use(db)

            utcnow = datetime.now(timezone.utc)
            api_timespan = utcnow - last_runutc

            seconds_span = api_timespan.total_seconds()
            if seconds_span < 4:
                sleep_time = 4 - seconds_span
                time.sleep(sleep_time)

        try_count = 0
        response = requests.Response

        try:
            while status_code > 299 and try_count < 5:
                try:
                    auth_header = {'Authorization': 'Bearer ' + current_app.config['STOCKS_API_TOKEN']}
                    response = requests.get(url_text, params=url_parameters, headers=auth_header)
                except ConnectionError as exc:
                    log_message = 'Exception-ConnectionError:: mboum API, during request, url: {}, params: {}'
                    utils.output_to_logfile(OutputLogType.apilog, log_message=log_message.format(url_text, str(url_parameters)), exception=exc)
                    break
                try_count += 1
                status_code = response.status_code
                if status_code == 404:
                    try_count = 6
                elif try_count > 1:
                    time.sleep(0.1025 + (try_count - 1) * 2)

            if status_code > 299 and try_count == 5:
                log_message = 'Error:: mboum API, tries exceeded, status code: {}, message: {}'.format(status_code, response.text)
                utils.output_to_logfile(OutputLogType.apilog, log_message=log_message)
                return {}
        except Exception as ex:
            log_message = 'Exception:: mboum API, uncaught error'
            utils.output_to_logfile(
                OutputLogType.apilog,
                log_message=log_message,
                exception=ex,
                trace=traceback.format_exc()
            )
        finally:
            with DatabaseSession() as db:
                history_add = SearchApiHistoryAdd(
                    api_name=API_NAME,
                    url_text=url_text,
                    url_parameters=str(url_parameters),
                    post_body='',
                    http_status=str(status_code),
                    platform_running=platform_name)

                status_filter = SearchApiStatusFilter(
                    api_name=API_NAME,
                    platform_running=platform_name
                )

                mboum_api_helper.__log_last_use(db, history_add)
                mboum_api_helper.__release_lock_mboum_api(db, status_filter)

        if 200 <= status_code <= 299:
            return response.json()
        else:
            log_message = 'Error:: mboum API, task-price-lookup, status code = {}, url: {}, params: {}'
            http_code = response.status_code
            utils.output_to_logfile(
                OutputLogType.errorlog,
                log_message=log_message.format(http_code, url_text, str(url_parameters)))

            return {}

    @staticmethod
    def __get_lock_mboum_api(db: Session, status_edit: SearchApiStatusEdit) -> bool:
        is_running = True
        num_tries = 0

        while is_running:
            results = (
                db.query(SearchApiStatusModel.api_name)
                .filter(SearchApiStatusModel.api_name == API_NAME)
                .filter(SearchApiStatusModel.is_running is False)
                .all())

            if len(results) > 0:
                is_running = False
            else:
                time.sleep(0.25)
                num_tries += 1

                if num_tries == (4 * 30):  # 30 seconds
                    message = 'Tried 5 times waiting for api lock'
                    utils.output_to_logfile(OutputLogType.errorlog,
                                            title='mboum API lock error',
                                            log_message=message)
                    return False

        statuses = (
            db.query(SearchApiStatusModel)
            .filter(SearchApiStatusModel.api_name == API_NAME)
            .all())

        if not statuses:
            message = 'Did not update search_api_status, lock on mboum'
            utils.output_to_logfile(OutputLogType.errorlog,
                                    title='mboum API lock error',
                                    log_message=message)
            return False

        status_update = status_edit.model_dump(exclude_unset=True)
        status_update['is_running'] = True
        for status in statuses:
            for key, value in status_update.items():
                setattr(status, key, value)

        db.commit()

        return True

    @staticmethod
    def __release_lock_mboum_api(db: Session, status_filter: SearchApiStatusFilter) -> bool:
        filters = status_filter.model_dump(exclude_unset=True)
        count = (
            db.query(SearchApiStatusModel)
            .filter_by(**filters)
            .update(
                {
                    SearchApiStatusModel.is_running: False,
                }, synchronize_session=False))

        if count == 0:
            message = 'Did not update search_api_status, lock on mboum'
            utils.output_to_logfile(OutputLogType.errorlog,
                                    title='mboum API lock error',
                                    log_message=message)
            return False

        return True

    @staticmethod
    def __get_last_use(db: Session) -> datetime:
        utcnow = datetime.now(timezone.utc)

        results = (
            db.query(SearchApiHistoryModel.createdutc)
            .filter(SearchApiHistoryModel.api_name == API_NAME)
            .order_by(SearchApiHistoryModel.createdutc.desc())
            .all())

        if len(results) == 0:
            return utcnow

        return results[0].createdutc

    @staticmethod
    def __log_last_use(db: Session, history_add: SearchApiHistoryAdd) -> None:
        history_insert = SearchApiHistoryModel(**history_add.model_dump())
        db.add(history_insert)
        db.commit()

        return
