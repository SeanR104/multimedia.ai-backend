import traceback
from flask import request

from system.exceptions import EFException, EFBadRequestException, EFServerException, EFAuthException
from utilities.utils import utils
from utilities.constants import OutputLogType


def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(exc):
        log_message = '{} {}, requested URL: {}, method: {}, content type: {},\nuser agent: {}'
        utils.output_to_logfile(
            OutputLogType.infolog,
            title='404 HTTP Response',
            log_message=log_message.format(
                exc.code,
                exc.name,
                request.url,
                request.method,
                request.content_type,
                request.user_agent
            ))

        exception_view = EFException()
        exception_view.status_code = 404
        exception_view.message = 'Page not found.'

        return utils.ok(exception_view.__dict__, exception_view.status_code)

    @app.errorhandler(405)
    def page_request_not_found(exc):
        log_message = '{} {}, requested URL: {}, method: {}, content type: {},\nuser agent: {}'
        utils.output_to_logfile(
            OutputLogType.infolog,
            title='405 HTTP Response',
            log_message=log_message.format(
                exc.code,
                exc.name,
                request.url,
                request.method,
                request.content_type,
                request.user_agent
            ))

        exception_view = EFException()
        exception_view.status_code = 405
        exception_view.message = 'Page request not found.'

        return utils.ok(exception_view.__dict__, exception_view.status_code)

    @app.errorhandler(Exception)
    def handle_exception(exc):
        if isinstance(exc, EFBadRequestException):
            exception_view = EFException()
            exception_view.status_code = exc.status_code
            exception_view.message = exc.message
        elif isinstance(exc, EFAuthException):
            exception_view = EFException()
            exception_view.status_code = exc.status_code
            exception_view.message = exc.message
        elif isinstance(exc, EFServerException):
            # log error to file
            utils.output_to_logfile(OutputLogType.errorlog, title='Server exception', exception=exc, trace=traceback.format_exc())

            exception_view = EFException()
            exception_view.status_code = exc.status_code
            exception_view.message = 'An unexpected error has occured.'
        else:
            # log error to file
            utils.output_to_logfile(OutputLogType.errorlog, title='Unhandled backend error', exception=exc, trace=traceback.format_exc())

            exception_view = EFException()
            exception_view.status_code = 500
            exception_view.message = 'An unexpected error has occured.'

        return utils.ok(exception_view.__dict__, exception_view.status_code)
