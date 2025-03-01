import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WSDL_URL_NAVIO = ''
    USERNAME = os.getenv("TCP_USERNAME", "default_user")
    PASSWORD = os.getenv("TCP_PASSWORD", "default_password")
    PORT = int(os.getenv("PORT", 3002))
    DATABASE_URI = os.getenv("DATABASE_URI")

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = os.getenv("DEV_DATABASE_URI")

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = os.getenv("PROD_DATABASE_URI")

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}