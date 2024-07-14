from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class LogEntry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String)
    message = Column(Text)


Base.metadata.create_all(engine)


def log_to_db(level, message):
    entry = LogEntry(level=level, message=message)
    session.add(entry)
    session.commit()


from loguru import logger

logger.add(log_to_db, level="DEBUG")
