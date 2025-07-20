from db.database import Base 
from sqlalchemy import Column,String, Text, Integer

class UserSchema(Base):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True,primary_key=True)
    username = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)