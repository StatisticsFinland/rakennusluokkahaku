from src import create_app
from src.question_selection import *
import pytest
from unittest import mock
from config import TestingConfig
from . import init_test_db


# @pytest.fixture
# def attributes():
#    attributes = {{'attribute_id': ['1', '101', '102'],
#                               'attribute_name': ['Asunnot', 'Asuinhuone',
#                                                  'Eteinen'],
#                               'attribute_question': ['Onko rakennuksessa asunnot?',
#                                                      'Onko rakennuksessa asuinhuone?',
#                                                      'Onko rakennuksessa eteinen?', ],
#                               'group_id': ['NaN', 'NaN', 'NaN'],
#                               'active': [False, False, False]})
#    return attributes
@pytest.fixture  # (scope='module')
def backend():
    app = create_app(TestingConfig)
    init_test_db(app)

    test_client = app.test_client()

    ctxt = app.app_context()
    ctxt.push()

    yield test_client

    ctxt.pop()


def test_best_questions_is_ordered(backend):
    with backend:
        questions = best_questions(None, [])
        for i in range(1, len(questions)):
            assert questions[i][1] >= questions[i - 1][1]


def test_for_simple_question_next_question_is_first_of_best_questions(backend):
    with backend:
        questions = best_questions(None, [])
        best_question = next_question(None, [])
        if best_question['type'] == 'simple':
            assert best_question['attribute_id'] == questions[0][0]


def test_non_active_attributes_are_not_selected(backend):
    #r = mock.Mock()
    #r.content = attributes
    # print(src.building_data.__dict__)
    # with mock.patch.('src.question_selection.src.building_data', '_attributes', new=attributes) as attr:
    #tmp = src.building_data._attributes_dict.copy()
    #src.building_data._attributes = attributes

    with backend:
        questions = best_questions(None, [])
        attribute_id = []
        for q in questions:
            attribute_id.append(q[0])
        assert '106' not in attribute_id

    #src.building_data._attributes = tmp


# def test_for_multi_question_first_of_best_questions_is_in_question_group():
#    questions = best_questions(None, [])
#    best_question = next_question(None, [])
#    if best_question['type'] == 'multi':
#        attributes = []
#        for attribute in best_question['attributes']:
#            attributes.append(attribute['attribute_id'])
#        assert questions[0][0] in attributes
