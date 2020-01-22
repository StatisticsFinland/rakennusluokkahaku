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


def test_if_admin_page_loads(backend):
    res = backend.get('/801fc3')
    assert("FaceTed-Man" in str(res.data))


def test_if_results_page_loads(backend):
    res = backend.get('/801fc3r')
    assert("Selected Class" in str(res.data))
