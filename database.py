from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    username = Column(String)

    def __init__(self, chat_id, username):
        self.chat_id = chat_id
        self.username = username

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
