from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from datetime import datetime

Base = declarative_base()


class UserQuestions(Base):
    __tablename__ = "user_questions"
    id = Column(Integer, primary_key=True)

    user = Column(String)
    question = Column(String)
    query = Column(String)
    query_plan = Column(String)
    query_errors = Column(String)
    query_explanation = Column(String)
    was_valid = Column(Boolean)

    marked_good = Column(Boolean, default=False)
    marked_bad = Column(Boolean, default=False)
    viewed_query = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=False), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=False), default=datetime.utcnow, onupdate=datetime.utcnow
    )
