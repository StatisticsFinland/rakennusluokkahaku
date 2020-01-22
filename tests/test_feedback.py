from flask import session
from src.models import Session
import pytest
from src import create_app
from . import init_test_db
from config import TestingConfig


@pytest.fixture
def backend():
    app = create_app(TestingConfig)
    init_test_db(app)

    test_client = app.test_client()

    ctxt = app.app_context()
    ctxt.push()

    yield test_client

    ctxt.pop()


def test_post_feedback_requires_json(backend):
    backend.get('/question')
    res = backend.post('/feedback')
    assert(res.get_json()['success'] == False)


def test_post_feedback_requires_class_id(backend):
    backend.get('/question')
    res = backend.post('/feedback', json={})
    assert(res.get_json()['success'] == False)


def test_post_feedback_requires_session(backend):
    with backend.session_transaction() as sess:
        sess.pop('user', None)
        assert 'user' not in sess
    res = backend.post('/feedback', json={
        'class_id': '0110'
    })
    assert(res.get_json()['success'] == False)


def test_post_feedback_succeeds(backend):
    backend.get('/question')
    res = backend.post('/feedback', json={
        'class_id': '0110'
    })
    assert(res.get_json()['success'] == True)


def test_post_feedback_ends_session(backend):
    with backend:
        backend.get('/question')
        assert 'user' in session
        backend.post('/feedback', json={
            'class_id': '0110'
        })
        assert 'user' not in session


def test_post_feedback_saves_selected_class(backend):
    users_session = None
    with backend:
        backend.get('/question')

        session_ident = session['user']
        users_session = Session.query.filter_by(
            session_ident=session_ident).first()

        assert users_session.selected_class == None
        backend.post('/feedback', json={
            'class_id': '0110'
        })
        assert users_session.selected_class.class_id == '0110'
