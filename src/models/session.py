from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db


class Session(db.Model):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    session_ident = Column(String, unique=True, nullable=False)
    buildclass_id = Column(Integer, ForeignKey(
        "building_class.id"), nullable=True)
    selected_class = relationship("BuildingClass")
    answered_questions = relationship(
        "AnswerQuestion", back_populates="session")

    def __repr__(self):
        return f"<Session(session_ident='{self.session_ident}', answered_questions='{self.answered_questions}')>"

    def __init__(self, sess):
        self.session_ident = sess

    def answered_questions_string(self):
        composed_string = ""
        for aq in self.answered_questions:
            composed_string += aq.attribute.attribute_id + " - " + aq.answer.value + ", "
        return composed_string
