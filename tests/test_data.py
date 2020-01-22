from src.building_data import *
import pytest


# @pytest.fixture
# def external_building_data():
#    return BuildingData('./data/')


# def test_observation_class_ids_in_building_classes(external_building_data):
#    observations = external_building_data.observations
#    building_class_name = external_building_data.building_class_name
#    for class_id in observations['class_id']:
#        assert class_id in building_class_name.keys()


# def test_observation_attribute_ids_in_attributes(external_building_data):
#    observations = external_building_data.observations
#    attribute_name = external_building_data.attribute_name
#    for attribute_id in observations.columns:
#        assert (attribute_id in ['class_id', 'count']) or \
#               (attribute_id in attribute_name.keys())


# def test_attribute_group_ids_in_attribute_groups(external_building_data):
#    attributes = external_building_data._attributes
#    attribute_groups = external_building_data.attribute_groups
#    for group_id in attributes['group_id'].dropna():
#        assert group_id in attribute_groups.group_id.values


# def test_attributes_are_loaded_from_file(external_building_data):
#    attributes = external_building_data._attributes
#    # Check that the loaded attributes are different from DEFAULT_ATTRIBUTES
#    assert (attributes.shape[0] != DEFAULT_ATTRIBUTES.shape[0]) or \
#           (attributes.shape[1] != DEFAULT_ATTRIBUTES.shape[1]) or \
#           (attributes.values != DEFAULT_ATTRIBUTES.values).any()


# def test_building_classes_are_loaded_from_file(external_building_data):
#    building_classes = external_building_data._building_classes
#    # Check that the loaded building classes are different from DEFAULT_ATTRIBUTES
#    assert (building_classes.shape[0] != DEFAULT_BUILDING_CLASSES.shape[0]) or \
#           (building_classes.shape[1] != DEFAULT_BUILDING_CLASSES.shape[1]) or \
#           (building_classes.values != DEFAULT_BUILDING_CLASSES.values).any()


# def test_observations_are_loaded_from_file(external_building_data):
#    observations = external_building_data.observations
#    # Check that the loaded observations are different from DEFAULT_OBSERVATIONS
#    assert (observations.shape[0] != DEFAULT_OBSERVATIONS.shape[0]) or \
#           (observations.shape[1] != DEFAULT_OBSERVATIONS.shape[1]) or \
#           (observations.values != DEFAULT_OBSERVATIONS.values).any()
