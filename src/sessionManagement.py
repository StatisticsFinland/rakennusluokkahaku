import uuid
from flask import session
import string
from datetime import date
from .models import db, Session

# to store every users session data
users = {}


def generate_id():
    '''Creates a unique UUID id and returns it in string form'''
    ident = uuid.uuid4()
    return str(ident)


def create_session():
    '''Creates and saves new session for user and returns session id'''
    ident = generate_id()
    session['user'] = ident
    users[ident] = {'user_responses': [],
                    'server_responses': [],
                    'created': date.today()}
    # Add the session to the database
    db.session.add(Session(ident))
    db.session.commit()
    return ident


def cleanup():
    today = date.today()
    old = []

    # Check outdated ones
    for one in users.keys():
        diff = today - users[one]['created']
        if diff.days >= 1:
            old.append(one)

    # Delete outdated ones
    for one in old:
        users.pop(one)
