import json
from flask import redirect, render_template, request, url_for
from flask_login import login_required

from . import views as app
from ..models import db, QuestionGroup


# Group view for listing active groups and adding new ones
@app.route("/801fc3/groups", methods=["GET", "POST"])
@login_required
def group_view():
    if request.method == "GET":
        return render_template("groupView.html", groups=QuestionGroup.query.all())

    form = request.form
    groupname = form.get('group_name')
    groupkey = form.get('group_key')
    fi = form.get('Suomeksi')
    sv = form.get('Svenska')
    en = form.get('English')

    question = '{"fi":"' + fi + '","sv":"' + sv + '","en":"' + en + '"}'
    try:
        json.loads(question)
        db.session.add(QuestionGroup(grouping_key=groupkey,
                                     group_name=groupname, group_question=question))
        db.session.commit()
        return render_template("groupView.html", groups=QuestionGroup.query.all())

    except:
        db.session.rollback()
        return render_template("groupView.html", groups=QuestionGroup.query.all(), error="Item could not be added, this might be due to use of quotes or a duplicate grouping key.")


# Edit Group question
@app.route("/edit_group_question/<group_id>", methods=["GET"])
@login_required
def edit_group_question_view(group_id):
    attribute = QuestionGroup.query.get(group_id)
    json_a = json.loads(attribute.group_question)
    return render_template("langTemplate.html", attribute=json_a, redirect_url=url_for('views.group_view'),
                           post_url=url_for('views.edit_group_question_string', group_id=attribute.id))


# group question edit handler
@app.route("/edit_group_question/<group_id>", methods=["POST"])
@login_required
def edit_group_question_string(group_id):
    group = QuestionGroup.query.get(group_id)

    try:
        form = request.form
        jsoned = json.loads(group.group_question)

        for key in jsoned:
            if(len(form[key]) > 0):
                jsoned[key] = form[key]

        group.group_question = json.dumps(jsoned)
        db.session.commit()
    except:
        print('Data parsing failed in group_question_edit')
        return redirect(url_for("views.group_view", error="Edit failed. This might be caused by quotes in the strings"))

    return redirect(url_for("views.group_view"))


# Edit Group name
@app.route("/edit_group_name/<group_id>", methods=["GET"])
@login_required
def edit_group_name_view(group_id):
    group = QuestionGroup.query.get(group_id)
    string = group.group_name
    return render_template("singleStringEditTemplate.html", string=string, redirect_url=url_for('views.group_view'),
                           post_url=url_for('views.edit_group_name_string', group_id=group.id))


# group name edit handler
@app.route("/edit_group_name/<group_id>", methods=["POST"])
@login_required
def edit_group_name_string(group_id):
    group = QuestionGroup.query.get(group_id)

    try:
        form = request.form
        string = group.group_name
        if len(form.get('string')) > 0:

            group.group_name = form.get('string')
            db.session.commit()
    except:
        print('Data parsing failed in group_name_edit')
        return redirect(url_for("views.group_view", error="Edit failed."))

    return redirect(url_for("views.group_view"))


# Edit Grouping key
@app.route("/edit_group_key/<group_id>", methods=["GET"])
@login_required
def edit_group_key_view(group_id):
    group = QuestionGroup.query.get(group_id)
    string = group.grouping_key
    return render_template("singleStringEditTemplate.html", string=string, redirect_url=url_for('views.group_view'),
                           post_url=url_for('views.edit_group_key', group_id=group.id))


# grouping key edit handler
@app.route("/edit_group_key/<group_id>", methods=["POST"])
@login_required
def edit_group_key(group_id):
    group = QuestionGroup.query.get(group_id)

    try:
        form = request.form
        string = group.grouping_key
        if len(form.get('string')) > 0:

            group.grouping_key = form.get('string')
            db.session.commit()
    except:
        print('Data parsing failed in group_name_edit')
        return redirect(url_for("views.group_view", error="Edit failed."))

    return redirect(url_for("views.group_view"))
