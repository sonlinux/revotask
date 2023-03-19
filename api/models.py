from sqlalchemy import Date, Column, Integer, String

from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    birthdate = Column(Date)
