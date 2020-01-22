import src
import json

from src.question_selection import next_question
from src.sessionManagement import users, create_session

from flask import jsonify, session, request
from . import views as app
from . import get_best_match_language, fix_question_language
from ..models import db, AnswerQuestion, Attribute, Session


@app.route('/previous', methods=['GET'])
def previous():
    best_match_language = get_best_match_language(request)
    # Create session if not already
    if 'user' not in session or session['user'] not in users:
        create_session()

    # Access users session data
    user = users[session['user']]

    # if user has no previous data a new question is created and saved
    if len(user['server_responses']) == 0:
        question = next_question(None, [])
        fix_question_language(question, best_match_language)
        user['server_responses'].append(question)
        return jsonify(question)

    elif len(user['server_responses']) == 1:
        question = user['server_responses'][-1]
        return jsonify(question)

    else:
        previous_attribute = ''
        question = None

        # if user returns to the first question, only the question is returned
        if len(user['server_responses']) == 2 and len(user['user_responses']) == 1:
            user['server_responses'].pop()
            previous_attribute = user['user_responses'][-1][0][0]
            user['user_responses'].pop()

            question = user['server_responses'][-1]

        if len(user['server_responses']) > 2 and len(user['user_responses']) > 1:
            user['server_responses'].pop()
            previous_attribute = user['user_responses'][-1][0][0]
            user['user_responses'].pop()

            question = user['server_responses'][-1]
            question['success'] = True

        # delete previous answer to the same question from database
        db_attribute = Attribute.query.filter_by(
            attribute_id=previous_attribute).first()
        db_session = Session.query.filter_by(
            session_ident=session['user']).first()
        session_answer_questions = db_session.answered_questions

        if db_attribute.grouping_id is not None:

            group_attributes = Attribute.query.filter_by(
                grouping_id=db_attribute.grouping_id).all()

            for attribute in group_attributes:
                try:
                    answer_question = next(
                        x for x in session_answer_questions if x.attribute_id == attribute.id)
                    db.session.delete(answer_question)
                    db.session.commit()
                except AttributeError as e:
                    print(
                        'Deletion of previous answer from database was not successful: ', e.args[0])
                    db.session.rollback()

        else:
            try:
                answer_question = session_answer_questions[-1]
                db.session.delete(answer_question)
                db.session.commit()
            except AttributeError as e:
                print(
                    'Deletion of previous answer from database was not successful: ', e.args[0])
                db.session.rollback()

        return jsonify(question)
