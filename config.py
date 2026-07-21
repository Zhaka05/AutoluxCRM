from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "hostname"
    database_port: str = "port"
    database_password: str = "password"
    database_name: str = "name"
    database_username: str = "username"
    secret_key: str = "secret_key"
    algorithm: str = "algorithm"
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()