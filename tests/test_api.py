import src
import src.models
from src.models import init_app
from src import create_app
from flask import session, jsonify
from src.sessionManagement import users
from src.models import Session, AnswerQuestion
from config import TestingConfig
import pytest
from . import init_test_db


@pytest.fixture  # (scope='module')
def backend():
    app = create_app(TestingConfig)
    init_test_db(app)

    test_client = app.test_client()

    ctxt = app.app_context()
    ctxt.push()

    yield test_client

    ctxt.pop()


@pytest.fixture
def responses(backend):

    responses = {'id': '', 'server_responses': [], 'user_responses': []}
    question_type = ''

    with backend:
        response = backend.get('/question')
        json = response.get_json()
        responses['id'] = session['user']
        question_type = json['type']
        responses['server_responses'].append(json)

        for x in range(2):

            answer = []
            attribute_id = []

            if question_type == 'simple':
                attribute = ''
                resp = responses['server_responses'][-1]
                if x == 0:
                    attribute = resp['attribute_id']
                elif x > 0:
                    attribute = resp['new_question']['attribute_id']
                answer.append('yes')
                attribute_id.append(attribute)
                response = backend.post(
                    '/answer', json={'language': 'fi', 'response': [{'attribute_id': attribute, 'response': 'yes'}]}
                )

            elif question_type == 'multi':
                attributes = []
                multi_answer = []
                if x == 0:
                    attributes = responses['server_responses'][-1]['attributes']
                elif x > 0:
                    attributes = responses['server_responses'][-1]['new_question']['attributes']

                for attribute in attributes:
                    res = {
                        'attribute_id': attribute['attribute_id'], 'response': 'no'}
                    attribute_id.append(attribute['attribute_id'])
                    multi_answer.append(res)
                    answer.append('no')
                response = backend.post(
                    '/answer', json={'language': 'fi', 'response': multi_answer}
                )
            json = response.get_json()
            new = {
                'new_question': json['new_question'],
                'building_classes': json['building_classes']
            }
            responses['server_responses'].append(new)
            responses['user_responses'].append(list(zip(attribute_id, answer)))

    return responses


def test_get_root_succeeds(backend):
    response = backend.get('/')
    assert response.status_code == 200


def test_get_question_succeeds(backend):
    response = backend.get('/question')
    assert response.status_code == 200


def test_get_question_returns_json(backend):
    response = backend.get('/question')
    json = response.get_json()
    if json['type'] == 'simple':
        assert 'attribute_id' in json
        assert 'attribute_name' in json
        assert 'attribute_tooltip' in json


def test_get_answer_fails(backend):
    response = backend.get('/answer')
    assert response.status_code == 405


def test_post_answer_succeeds(backend):
    response = backend.post('/answer')
    assert response.status_code == 200


def test_post_answer_requires_sent_json(backend):
    response = backend.post('/answer')
    json = response.get_json()
    assert json['success'] == False


def test_post_answer_requires_all_fields(backend):
    response = backend.post('/answer', json={})
    json = response.get_json()
    assert json['success'] == False

    response = backend.post('/answer', json={'attribute_id': '1'})
    json = response.get_json()
    assert json['success'] == False

    response = backend.post(
        '/answer', json={"language": "fi", "response": [{"attribute_id": "1", "response": "yes"}]}
    )
    json = response.get_json()
    assert json['success'] == True


def test_post_answer_returns_new_question(backend):
    response = backend.post(
        '/answer', json={"language": "fi", "response": [{"attribute_id": "1", "response": "yes"}]}
    )
    json = response.get_json()
    assert 'new_question' in json
    assert 'type' in json['new_question']
    assert 'attribute_question' in json['new_question']
    if json['new_question']['type'] == 'simple':
        assert 'attribute_id' in json['new_question']
        assert 'attribute_name' in json['new_question']
        assert 'attribute_tooltip' in json['new_question']


def test_post_answer_returns_building_classes(backend):
    with backend:
        response = backend.post(
            '/answer', json={"language": "fi", "response": [{"attribute_id": "1", "response": "yes"}]}
        )
        json = response.get_json()
        assert 'building_classes' in json
        for item in json['building_classes']:
            assert 'class_id' in item
            assert 'class_name' in item
            assert 'score' in item


def test_session_gets_created_for_client_requesting_first_question(backend):
    with backend.session_transaction() as sess:
        sess.pop('user', None)
        assert 'user' not in sess
    with backend:
        backend.get('/question')
        assert 'user' in session


def test_id_stored_in_session_is_string(backend):
    with backend:
        backend.get('/question')
        assert isinstance(session['user'], str)


def test_session_gets_recreated_for_client_requesting_first_question(backend):
    previous_id = ''
    with backend:
        backend.get('/question')
        with backend.session_transaction() as sess:
            previous_id = sess['user']
        backend.get('/question')
        assert previous_id != ''
        assert session['user'] != previous_id


def test_if_user_in_session_user_data_is_created_after_first_question(backend):
    with backend:
        response = backend.get('/question')
        json = response.get_json()
        if json['type'] == 'simple':
            attribute_id = json['attribute_id']
            users.pop(session['user'], None)
            assert session['user'] not in users
            backend.post(
                '/answer', json={"language": "fi", "response": [{"attribute_id": attribute_id, "response": "yes"}]}
            )
            assert session['user'] in users


def test_same_questions_not_repeated_during_session(responses):
    total_attributes = []
    for response in responses['user_responses']:
        for pair in response:
            total_attributes.append(pair[0])
    unique_attributes = list(set(total_attributes))
    assert len(unique_attributes) == len(total_attributes)


def test_prior_server_responses_are_saved_during_session(responses):
    user = users[responses['id']]
    assert len(user['server_responses']) == len(responses['server_responses'])


def test_user_responses_are_saved_during_session(responses):
    user = users[responses['id']]
    assert user['user_responses'] == responses['user_responses']


def test_building_clases_are_saved_during_session(responses):
    user = users[responses['id']]
    user_classes = []
    test_classes = []
    for response in user['server_responses']:
        if 'building_classes' in response:
            user_classes.append(response['building_classes'])
    for response in responses['server_responses']:
        if 'building_classes' in response:
            test_classes.append(response['building_classes'])
    assert len(user_classes) == len(test_classes)


def test_returned_building_classes_are_based_on_prior_probabilities(backend):
    attribute_id = ''
    response = ''
    prior = ''
    posterior = ''
    building_classes = []
    new_building_classes = []
    with backend:
        response = backend.get('/question')
        json = response.get_json()
        print('Response 1:', json)
        if json['type'] == 'simple':
            attribute_id = json['attribute_id']
            prob = src.classifier.calculate_posterior(
                [attribute_id], ['yes'], None)
            prior = prob['posterior']
            response = backend.post(
                '/answer', json={"language": "fi", "response": [{"attribute_id": attribute_id, "response": "yes"}]})
            json = response.get_json()
            print('Response 2:', json)
            print('Prob 2:', prob)
            attribute_id = json['new_question']['attribute_id']
            posterior = src.classifier.calculate_posterior(
                [attribute_id], ['yes'], prior)
            response = backend.post(
                '/answer', json={"language": "fi", "response": [{"attribute_id": attribute_id, "response": "yes"}]})
            json = response.get_json()
            print('Response 3:', json)
            print('Prob 3:', posterior)
            building_classes = json['building_classes']
            for _, (class_id, score) in posterior.iterrows():
                if class_id in src.building_data.building_class_name:
                    new_building_classes.append({'class_id': class_id,
                                                 'class_name': src.building_data.building_class_name[class_id],
                                                 'score': score})
            print('building_classes:', building_classes)
            print('new_building_classes:', new_building_classes)
            assert building_classes == new_building_classes


def test_requesting_previous_question_returns_correct_question(responses, backend):
    previous_question = responses['server_responses'][-2]['new_question']
    previous_attribute = None
    attribute_name = ''
    previous_question_string = previous_question['attribute_question']
    if previous_question['type'] == 'simple':
        previous_attribute = previous_question['attribute_id']
        attribute_name = previous_question['attribute_name']
    else:
        previous_attribute = previous_question['attributes']
    with backend:
        response = backend.get('/previous')
        json = response.get_json()
        if json['new_question']['type'] == 'simple':
            attribute = json['new_question']['attribute_name']
            attribute_id = json['new_question']['attribute_id']
            question_string = json['new_question']['attribute_question']
            assert attribute == attribute_name
            assert attribute_id == previous_attribute
            assert question_string == previous_question_string
        else:
            attribute = json['new_question']['attributes']
            assert attribute == previous_attribute


def test_if_user_returs_to_first_question_no_building_classes_are_sent(backend):
    with backend:
        response = backend.get('/question')
        json = response.get_json()
        if json['type'] == 'simple':
            question = json['attribute_name']
            attribute_id = json['attribute_id']
            backend.post(
                '/answer', json={"language": "fi", "response": [{"attribute_id": attribute_id, "response": "yes"}]})
            previous = backend.get('/previous')
            json = previous.get_json()
            assert 'building_classes' not in json
            assert json['attribute_name'] == question


def test_if_user_presses_return_during_first_question_same_question_is_returned(backend):
    with backend:
        response = backend.get('/question')
        response_json = response.get_json()
        previous = backend.get('/previous')
        previous_json = previous.get_json()
        assert response_json == previous_json


def test_if_user_in_session_user_data_is_created_when_asking_previous_question(backend):
    with backend:
        response = backend.get('/question')
        json = response.get_json()
        if json['type'] == 'simple':
            attribute_id = json['attribute_id']
            backend.post(
                '/answer', json={"language": "fi", "response": [{"attribute_id": attribute_id, "response": "yes"}]})
            users.pop(session['user'], None)
            assert session['user'] not in users
            backend.get('/previous')
            assert session['user'] in users


def test_get_question_adds_session_to_database(backend):
    with backend:
        sessions_old = Session.query.all()
        backend.get('/question')
        sessions_new = Session.query.all()

        assert len(sessions_new) == len(sessions_old) + 1
        assert sessions_new[-1].session_ident == session['user']


def test_post_feedback_adds_answers_to_database(backend):
    with backend:
        response = backend.get('/question')
        sessions = Session.query.all()
        print('response:', response.get_json())

        attribute_id = response.get_json()['attribute_id']

        answer_question_old = AnswerQuestion.query.all()
        backend.post(
            '/answer', json={"language": "fi", "response": [{'attribute_id': attribute_id, 'response': 'yes'}]})

        backend.post('/feedback', json={
            'class_id': '0110'
        })

        answer_question_new = AnswerQuestion.query.all()

        assert len(answer_question_new) == len(answer_question_old) + 1
        assert answer_question_new[-1].session_id == sessions[-1].id
        assert answer_question_new[-1].attribute.attribute_id == attribute_id
        assert answer_question_new[-1].answer.value == 'yes'


def test_previous_deletes_answers_from_database(backend, responses):
    answer_question_old = AnswerQuestion.query.all()
    with backend:
        backend.get('/previous')
        answer_question_new = AnswerQuestion.query.all()
        assert len(answer_question_new) == len(answer_question_old) - 1
        assert answer_question_new[-1].attribute.attribute_id == answer_question_old[-2].attribute.attribute_id
        assert answer_question_new[-1].answer.value == answer_question_old[-2].answer.value


@pytest.fixture
def clean_backend():
    app = create_app(TestingConfig)
    init_test_db(app)

    test_client = app.test_client()

    ctxt = app.app_context()
    ctxt.push()

    yield test_client

    ctxt.pop()


def test_initially_database_contains_no_sessions(clean_backend):
    with clean_backend:
        sessions = Session.query.all()
        assert len(sessions) == 0
