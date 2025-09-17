import os

from urllib.parse import quote


class BaseConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False

    def __init__(self):
        db_user = quote(os.getenv("DB_USER", "user"))
        db_password = quote(os.getenv("DB_PASSWORD", "pass"))
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = quote(os.getenv("DB_NAME", "database"))
        db_timeout = os.getenv("DB_TIMEOUT", "10")
        db_sslmode = os.getenv("DB_SSLMODE", "prefer")

        self.SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            f"?connect_timeout={db_timeout}&sslmode={db_sslmode}"
        )

        self.APP_NAME = os.getenv("APP_NAME", "backend-stock-api-default")
        self.API_LOG_PATH = os.getenv("API_LOG_PATH", "logs/api.log")
        self.INFO_LOG_PATH = os.getenv("INFO_LOG_PATH", "logs/info.log")
        self.ERROR_LOG_PATH = os.getenv("ERROR_LOG_PATH", "logs/error.log")

        self.STOCKS_API_BASE_URL = os.getenv("STOCKS_API_BASE_URL")
        self.STOCKS_API_TOKEN = os.getenv("STOCKS_API_TOKEN")


class LocalConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_ECHO = False


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
