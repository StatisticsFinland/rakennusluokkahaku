from flask import request, jsonify, session

from . import views as app
from src.sessionManagement import users
from src.models import db, BuildingClass, Session


@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        content = request.get_json()
        class_id = content['class_id']
    except TypeError:
        return jsonify({'success': False,
                        'message': 'Please supply "class_id" in query'})
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Please supply "class_id" in query'})
    else:
        if 'user' in session:
            # Save selected building class to database
            sess = Session.query.filter_by(
                session_ident=session['user']).first()
            selected_class = BuildingClass.query.filter_by(
                class_id=class_id).first()
            sess.selected_class = selected_class
            db.session.commit()

            # Remove session and data related to it
            users.pop(session['user'], None)
            session.pop('user', None)

            return jsonify({'success': True})

        return jsonify({'success': False})
