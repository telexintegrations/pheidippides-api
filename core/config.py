from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pheidippides API"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "An integration that suggests books to read based on any selected genre."
    API_PREFIX: str = "/pheidippides-api"
    

settings = Settings()