from flask_sqlalchemy import SQLAlchemy

# Create db object
db = SQLAlchemy()

# Note these must be imported after creating the db object, since they use
# db.Model as a superclass
from .building_class import BuildingClass
from .attribute import Attribute
from .answer import Answer
from .answer_question import AnswerQuestion
from .session import Session
from .question_grouper import QuestionGroup
from .admin import Admin
from .buildingclass_attribute import ClassAttribute


def init_app(app):
    '''Initializes the database using the provided app'''
    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print('Failed to create tables:', e)
