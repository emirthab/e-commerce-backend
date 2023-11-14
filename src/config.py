import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    WRITER_DB_URL: str = f"mysql+aiomysql://user:pass@db:3306/database"
    READER_DB_URL: str = f"mysql+aiomysql://user:pass@db:3306/database"
    
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    
    CELERY_BROKER_URL: str = "amqp://user:bitnami@rabbitmq:5672/"
    CELERY_BACKEND_URL: str = "redis://redis:6379"
    
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""
    
    OTP_CODE_EXPIRY_MINUTE: int = 5
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_ADDRESS: str = ""
    
    FIREBASE_STORAGE_URL: str = ""

class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f""
    READER_DB_URL: str = f""


class LocalConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://user:pass@20.79.221.139:3306/database"
    READER_DB_URL: str = f"mysql+aiomysql://user:pass@20.79.221.139:3306/database"
    
    CELERY_BROKER_URL: str = "amqp://user:bitnami@20.79.221.139:5672/"
    CELERY_BACKEND_URL: str = "redis://127.0.0.1"
    
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""


class ProductionConfig(Config):
    DEBUG: bool = False
    WRITER_DB_URL: str = f"mysql+aiomysql://user:pass@db:3306/database"
    READER_DB_URL: str = f"mysql+aiomysql://user:pass@db:3306/database"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
