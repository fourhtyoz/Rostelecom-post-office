from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

DB = 'sqlite:///.database.db/'
engine = create_engine(DB)
Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    lname = Column(String)
    fname = Column(String)
    mname = Column(String)
    phone = Column(Integer)
    message = Column(String)
