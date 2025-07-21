from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from config import settings

DB_URL = settings.DB_URL

# 1. TO CONNECT TO A DATABASE
engine = create_engine(DB_URL)

#2.SESSION MAKER WILL CREATE A SESSION AND TALK TO DB
SESSION_MAKER = sessionmaker(engine,autoflush=False)

# 3. BASE IS USED TO CREATE TABLES
Base = declarative_base()

def get_db():
    try:
        db = SESSION_MAKER()
        yield db 
    finally:
        db.close()
