from sqlalchemy import Column, Integer, Table, ForeignKey, DateTime, func, Float, Boolean
from sqlalchemy.orm import relationship
from . import db


class ClassAttribute(db.Model):
    __tablename__ = 'class_attribute'

    id = Column(Integer, primary_key=True)
    custom_probability = Column(Float, nullable=True)
    class_has_attribute = Column(Boolean, nullable=False)

    attribute_id = Column(Integer, ForeignKey('attribute.id'))
    buildingclass_id = Column(Integer, ForeignKey('building_class.id'))
    attribute = relationship("Attribute")
    building_class = relationship("BuildingClass")

    def __init__(self, attribute, building_class, has_attribute=False, custom_probability=None):
        self.attribute_id = attribute.id
        self.buildingclass_id = building_class.id
        self.class_has_attribute = has_attribute
        self.custom_probability = custom_probability

    def __repr__(self):
        return f"<ClassAttribute(attribute_id='{self.attribute_id}', buildindclass_id='{self.buildingclass_id}', class_has_attribute={self.class_has_attribute}, custom_probability={self.custom_probability})>"
