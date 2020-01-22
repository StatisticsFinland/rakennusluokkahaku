from sqlalchemy import Column, Integer, String
from . import db


class Answer(db.Model):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    value = Column(String(12), nullable=False, unique=True)

    def __repr__(self):
        return f"<Answer(value='{self.value}')>"
