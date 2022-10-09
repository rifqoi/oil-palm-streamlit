from pydantic import BaseSettings
from dotenv import dotenv_values, load_dotenv


class Settings(BaseSettings):
    load_dotenv()
    env = dotenv_values()

    COOKIE_NAME = env.get("COOKIE_NAME")
    COOKIE_EXPIRY_DAYS = int(env.get("COOKIE_EXPIRY_DAYS"))
    API_URL = env.get("API_URL")

    JWT_SECRET = env.get("JWT_SECRET")


settings = Settings()
