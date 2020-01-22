from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from . import db
from .question_grouper import QuestionGroup


class Attribute(db.Model):
    __tablename__ = 'attribute'

    id = Column(Integer, primary_key=True)
    attribute_id = Column(String(12), nullable=False, unique=True)
    attribute_name = Column(String(1000), nullable=False)
    attribute_question = Column(String(1000), nullable=False)
    grouping_id = Column(Integer, ForeignKey(
        "question_group.id"), nullable=True)
    part_of_group = relationship("QuestionGroup")
    active = Column(Boolean, nullable=True)
    attribute_tooltip = Column(String(1000), nullable=True)
    probability = Column(Float, nullable=False)

    def __init__(self, id_, name, question, tooltip=None, probability=0.5, active=False, group=None):
        self.attribute_id = id_
        self.attribute_name = name
        self.attribute_question = question
        self.attribute_tooltip = tooltip
        self.probability = probability
        self.active = active

        if group is None:
            self.grouping_id = None
        elif isinstance(group, str):
            group = QuestionGroup.query.filter_by(grouping_key=group).first()
            self.grouping_id = group.id
        elif isinstance(group, QuestionGroup):
            self.grouping_id = group.id

    def __repr__(self):
        return f"<Attribute(attribute_id='{self.attribute_id}', attribute_name='{self.attribute_name}', attribute_question='{self.attribute_question}')>"
