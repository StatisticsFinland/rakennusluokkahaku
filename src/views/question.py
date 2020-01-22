import json
from src.sessionManagement import create_session, cleanup, users
from src.question_selection import next_question
from flask import jsonify, session, request
from . import views as app
from . import fix_question_language, get_best_match_language


@app.route('/question', methods=['GET'])
def question():
    best_match_language = get_best_match_language(request)

    # Remove users previous state
    if 'user' in session:
        users.pop(session['user'], None)

    ident = create_session()
    question = next_question(None, [])
    fix_question_language(question, best_match_language)

    # Save response
    users[ident]['server_responses'].append(question)

    # Cleanup users dict
    cleanup()

    return jsonify(question)
