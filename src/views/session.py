import os
from flask import render_template, request, send_file
from flask_login import login_required
import pandas as pd
from sqlalchemy import func

from . import views as app
from ..models import db, Answer, AnswerQuestion, Attribute, BuildingClass, Session


# results view
@app.route("/801fc3r", methods=["GET"])
@login_required
def results_view():
    # Change default_minimum to 0 if you want to always see empty sessions by default, or some other number if you want the filtering to be rougher.
    # For a quick temporary filter- In the browser, you can use /801fc3r?min=5 for example, to set the filter to only show sessions with 5 or more answered questions
    default_minimum = 1
    count = request.args.get('min')
    try:
        if count:
            count = max(int(count), default_minimum)
        else:
            count = default_minimum
    except:
        count = default_minimum

    return render_template("resultsView.html", sessions=Session.query
                           .outerjoin(AnswerQuestion)
                           .group_by(Session)
                           .having(func.count_(Session.answered_questions) >= count)
                           .all()
                           )


@app.route("/801fc3s", methods=["GET"])
@login_required
def session_view():
    session_id = request.args.get('session')

    sess = Session.query.get(session_id)
    return render_template("sessionView.html", session=sess)


def create_session_data_file(search_string, count=1):
    attributes = Attribute.query.all()

    sessions = Session.query\
                      .filter((Session.session_ident.contains(search_string)) |
                              (Session.selected_class.has(BuildingClass.class_id.contains(search_string))) |
                              (Session.answered_questions.any((AnswerQuestion.attribute.has(Attribute.attribute_id.contains(search_string))) |
                                                              (AnswerQuestion.answer.has(Answer.value.contains(search_string))))))\
                      .outerjoin(AnswerQuestion)\
                      .group_by(Session)\
                      .having(func.count_(Session.answered_questions) >= count)\
                      .all()

    columns = {'session_id': [x.session_ident for x in sessions],
               'selected_class': [x.selected_class.class_id if x.selected_class is not None else '-' for x in sessions]}
    attr_columns = {x.attribute_id: '-' for x in attributes}
    columns.update(attr_columns)

    df = pd.DataFrame(columns)
    df = df.set_index('session_id')

    for x in sessions:
        for y in x.answered_questions:
            df.loc[x.session_ident, y.attribute.attribute_id] = y.answer.value

    df.to_csv('./tmp/session_export.csv')

    return './tmp/session_export.csv'

# Export session data handler
@app.route('/session_export', methods=['POST'])
@login_required
def session_export():
    form = request.form
    search_string = form.get('search_string', '')
    try:
        count = int(form.get('count', 1))
    except:
        count = 1
    filename = create_session_data_file(search_string, count)
    filename = os.path.abspath(filename)

    return send_file(filename, mimetype='text/csv', as_attachment=True)
