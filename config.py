import os
from dotenv import load_dotenv
from pathlib import Path


env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_TITLE : str = "Portfolio"
    SESSION_SECRET_KEY : str  = os.getenv("SESSION_SECRET_KEY")
    JWT_SECRET_KEY : str  = os.getenv("JWT_SECRET_KEY")
    DB_NAME : str  = os.getenv("DB_NAME")   
    DB_URL = f"sqlite:///{DB_NAME}.db"
settings = Settings()
