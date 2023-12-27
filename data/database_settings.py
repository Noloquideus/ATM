from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    class Config:
        env_file = ".env"


# We create an instance of a class that loads values from the .env file
db_settings = DatabaseSettings()

# Now you can get the values of variables as attributes of a class instance
DATABASE_HOST = db_settings.DATABASE_HOST
DATABASE_PORT = db_settings.DATABASE_PORT
DATABASE_NAME = db_settings.DATABASE_NAME
DATABASE_USER = db_settings.DATABASE_USER
DATABASE_PASSWORD = db_settings.DATABASE_PASSWORD
