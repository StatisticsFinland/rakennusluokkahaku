import src
import json
import numpy as np

from src.question_selection import next_question
from src.sessionManagement import users, create_session

from flask import request, jsonify, session
from . import views as app
from . import fix_question_language, validate_language
from ..models import db, Answer, AnswerQuestion, Attribute, Session


@app.route('/answer', methods=['POST'])
def answer():
    try:
        content = request.get_json()

        language = content['language']
        best_match_language = validate_language(language)

        attribute_id = []
        response = []
        for resp in content['response']:
            attribute_id.append(resp['attribute_id'])
            response.append(resp['response'])

    except TypeError:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "attribute_id", and "response" in query'})
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "attribute_id", and "response" in query'})
    else:
        # Create session if not already
        if 'user' not in session or session['user'] not in users:
            create_session()

        # Access users session data
        user = users[session['user']]

        # Save user responses
        user['user_responses'].append(list(zip(attribute_id, response)))
        # Add the responses to the database. First find the appropriate rows
        # from attribute, answer, and session tables, then create the new
        # AnswerQuestion
        for (attribute, resp) in user['user_responses'][-1]:
            try:
                db_attribute = Attribute.query.filter_by(
                    attribute_id=attribute).first()
                db_answer = Answer.query.filter_by(value=resp).first()
                db_session = Session.query.filter_by(
                    session_ident=session['user']).first()
                db.session.add(AnswerQuestion(
                    db_attribute, db_answer, db_session))
                db.session.commit()
            except AttributeError as e:
                print(
                    'It seems one or more of attribute, answer or session have not been populated correctly:', e.args[0])
                db.session.rollback()

        # Select the previous probabilities as prior for calculating posterior
        prior = None
        if len(user['server_responses']) > 1:
            prior = []
            for one in user['server_responses'][-1]['building_classes']:
                prior.append(one['score'])
            prior = np.array(prior)

        # Calculate new probabilities for building classes
        posterior = src.classifier.calculate_posterior(
            attribute_id, response, prior)
        new_building_classes = []

        for _, (class_id, score) in posterior.iterrows():
            if class_id in src.building_data.building_class_name:
                new_building_classes.append({'class_id': class_id,
                                             'class_name': src.building_data.building_class_name[class_id],
                                             'score': score})

        # Find out which attributes have been asked already
        asked_attributes = []
        for resp in user['user_responses']:
            for one in resp:
                asked_attributes.append(one[0])

        question = next_question(prior, asked_attributes)
        fix_question_language(question, best_match_language)

        json = {
            'new_question': question,
            'building_classes': new_building_classes
        }
        # Save response
        user['server_responses'].append(json)
        json['success'] = True
        return jsonify(json)
