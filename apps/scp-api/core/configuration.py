from yaml import safe_load
from pydantic import BaseModel
from os.path import expandvars


class DatabaseSettings(BaseModel):
    uri: str = "postgresql:///?User=root&Database=postgres&Server=127.0.0.1&Port=5432"


class AppSettings(BaseModel):
    name: str = "default"
    host: str = "127.0.0.1"
    port: int = 8000
    version: str = "1.0.1"


class Settings(BaseModel):
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()


with open("config.yaml", 'r') as file:
    try:
        config = file.read()
    except Exception as e:
        print(e)

settings = Settings(**safe_load(expandvars(config)))