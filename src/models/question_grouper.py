from sqlalchemy import Column, Integer, String
from . import db


class QuestionGroup(db.Model):
    __tablename__ = 'question_group'

    id = Column(Integer, primary_key=True)
    grouping_key = Column(String(24), nullable=False, unique=True)
    group_name = Column(String(64), nullable=False)
    group_question = Column(String(64), nullable=False)

    def __repr__(self):
        return f"<QuestionGroup(grouping_key='{self.grouping_key}, group_name='{self.group_name}', group_question='{self.group_question}')>"
