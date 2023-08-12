from pydantic_settings import BaseSettings    # PydanticUserError
from pydantic import EmailStr


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str
    redis_port: int
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DOMAIN: str
    DB_NAME: str
    DB_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
