from sqlalchemy import Column, Integer, String, Float
from . import db


class BuildingClass(db.Model):
    __tablename__ = 'building_class'

    id = Column(Integer, primary_key=True)
    class_id = Column(String(24), nullable=False, unique=True)
    class_name = Column(String(64), nullable=False)
    class_probability = Column(Float, nullable=False)

    def __repr__(self):
        return f"<BuildingClass(class_id='{self.class_id}', class_name='{self.class_name}', class_probability={self.class_probability})>"
