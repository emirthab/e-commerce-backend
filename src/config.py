import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    WRITER_DB_URL: str = f"mysql+aiomysql://newyork:newyork123@db:3306/newyork"
    READER_DB_URL: str = f"mysql+aiomysql://newyork:newyork123@db:3306/newyork"
    
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    
    CELERY_BROKER_URL: str = "amqp://user:bitnami@rabbitmq:5672/"
    CELERY_BACKEND_URL: str = "redis://redis:6379"
    
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""
    
    OTP_CODE_EXPIRY_MINUTE: int = 5
    SMTP_HOST: str = "smtp.office365.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_ADDRESS: str = ""
    
    FIREBASE_STORAGE_URL: str = "https://storage.googleapis.com/new-york-42e41.appspot.com/"

class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://newyork:newyork123@db:3306/newyork"
    READER_DB_URL: str = f"mysql+aiomysql://newyork:newyork123@db:3306/newyork"


class LocalConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://newyork:newyork123@0.0.0.0:3306/newyork"
    READER_DB_URL: str = f"mysql+aiomysql://newyork:newyork123@0.0.0.0:3306/newyork"
    
    CELERY_BROKER_URL: str = "amqp://user:bitnami@0.0.0.0:5672/"
    CELERY_BACKEND_URL: str = "redis://0.0.0.0:6379"
    
    REDIS_HOST: str = "0.0.0.0"
    REDIS_PORT: int = 6379
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""


class ProductionConfig(Config):
    DEBUG: bool = False
    WRITER_DB_URL: str = f"mysql+aiomysql://newyork:newyork123@db:3306/newyork"
    READER_DB_URL: str = f"mysql+aiomysql://newyork:newyork123@db:3306/newyork"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
