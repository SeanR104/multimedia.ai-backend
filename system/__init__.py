from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from system import config
from system.config import LocalConfig, DevelopmentConfig, ProductionConfig, TestingConfig
from system.database import init_engine
from system.register_error_handlers import register_error_handlers
from system.register_loggers import register_loggers


def create_app(env=None):
    if env is not None:
        dotenv_file = f".env.{env}"
        load_dotenv(dotenv_file, override=True)

    config_map = {
        "local": LocalConfig,
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    config_obj = config_map.get(env, LocalConfig)
    config_instance = config_obj()

    app = Flask(__name__)
    app.config.from_object(config_instance)

    logger = register_loggers(
        app_name=app.config['APP_NAME'],
        path_to_folder_api=app.config['API_LOG_PATH'],
        path_to_folder_info=app.config['INFO_LOG_PATH'],
        path_to_folder_error=app.config['ERROR_LOG_PATH']
    )
    if len(logger.handlers) < 3:
        logger.critical("Logging not configured. Quitting.")
        return None

    try:
        init_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=app.config["SQLALCHEMY_ECHO"])
    except Exception as e:
        logger.critical(f"Failed to initialize database: {e}")
        return None

    CORS(app)

    register_error_handlers(app)

    # web endpoints
    from controllers.web import auth_bp, users_bp
    app.register_blueprint(auth_bp, url_prefix='/web/auth')
    app.register_blueprint(users_bp, url_prefix='/web/users')

    # api endpoints v1
    from controllers.api.v1 import companies_bp, markets_bp, options_bp, stocks_bp
    app.register_blueprint(companies_bp, url_prefix='/api/v1/companies')
    app.register_blueprint(markets_bp, url_prefix='/api/v1/markets')
    app.register_blueprint(options_bp, url_prefix='/api/v1/options')
    app.register_blueprint(stocks_bp, url_prefix='/api/v1/stocks')

    return app
