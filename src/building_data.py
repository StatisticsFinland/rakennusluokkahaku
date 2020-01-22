import os
import sys
import numpy as np
import pandas as pd

from .models import Attribute, BuildingClass, QuestionGroup


class BuildingData:
    def __init__(self, app=None):
        '''Initializes empty BuildingData object'''
        # Store app for creating contexts
        self.app = app

        # Initialize the cache dicts as empty
        self._building_classes_dict = {}
        self._attributes_dict = {}
        self._attributes_names_dict = {}

    def load_from_db(self):
        with self.app.app_context():
            # Load building classes
            building_classes = BuildingClass.query.all()
            self._building_classes_dict = {
                x.class_id: x.class_name for x in building_classes}

            # Load attributes
            attributes = Attribute.query.all()
            self._attributes_names_dict = {
                x.attribute_id: x.attribute_name for x in attributes}
            self._attributes_dict = {x.attribute_id: {'attribute_id': x.attribute_id,
                                                      'attribute_name': x.attribute_name,
                                                      'attribute_question': x.attribute_question,
                                                      'group_id': x.part_of_group.grouping_key if x.grouping_id is not None else None,
                                                      'active': x.active,
                                                      'attribute_tooltip': x.attribute_tooltip} for x in attributes}

            # Load attribute groups
            # FIXME: remove pandas depedency
            attribute_groups = QuestionGroup.query.all()
            self.attribute_groups = pd.DataFrame([{'group_id': x.grouping_key,
                                                   'group_name': x.group_name,
                                                   'group_question': x.group_question} for x in attribute_groups])

    @property
    def attribute(self):
        '''Returns the attribute_id to attribute fields dict mapping'''
        return self._attributes_dict

    @property
    def attribute_name(self):
        '''Returns the attribute_id-attribute_name mapping'''
        return self._attributes_names_dict

    @property
    def building_class_name(self):
        '''Returns the building class_id-class_name mapping'''
        return self._building_classes_dict
