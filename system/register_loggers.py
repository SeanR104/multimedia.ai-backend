import os
import sys
import logging
import traceback


def register_loggers(app_name: str, path_to_folder_api: str, path_to_folder_info: str, path_to_folder_error: str):
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.CRITICAL)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        os.makedirs(path_to_folder_api, exist_ok=True)
        os.makedirs(path_to_folder_info, exist_ok=True)
        os.makedirs(path_to_folder_error, exist_ok=True)

        full_path_api_log = os.path.join(path_to_folder_api, 'api.log')
        full_path_info_log = os.path.join(path_to_folder_info, 'info.log')
        full_path_error_log = os.path.join(path_to_folder_error, 'error.log')

        api_handler = logging.FileHandler(full_path_api_log)
        api_handler.setLevel(logging.DEBUG)
        api_handler.addFilter(lambda r: r.levelno == logging.DEBUG)
        api_handler.setFormatter(formatter)

        info_handler = logging.FileHandler(full_path_info_log)
        info_handler.setLevel(logging.INFO)
        info_handler.addFilter(lambda r: r.levelno == logging.INFO)
        info_handler.setFormatter(formatter)

        error_handler = logging.FileHandler(full_path_error_log)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        logger.addHandler(api_handler)
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)

    except Exception as ex:
        exception_log = 'Exception Thrown:: failed to setup logger.\nException: {}\nStack Trace: {}'
        exception_message = str(type(ex)) + '\n'
        exception_message += str(ex).partition('\n')[0]
        logger.critical(exception_log.format(exception_message, traceback.format_exc()))

    return logger
