import json
from flask import redirect, render_template, request, url_for
from flask_login import login_required

from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, SelectField, StringField, validators
from wtforms.validators import ValidationError

from . import views as app
from ..models import db, Attribute, BuildingClass, ClassAttribute, QuestionGroup


# Attributes view
@app.route("/801fc3", methods=["GET"])
@login_required
def admin_view():
    groups = QuestionGroup.query.all()

    error = request.args.get('error', '')
    success = request.args.get('success', '')

    form = AttributeForm()
    form.attribute_group_id.choices += [
        (x.grouping_key, f'{x.grouping_key} - {x.group_name}') for x in groups]

    return render_template("admView.html",
                           attributes=Attribute.query.all(),
                           groups=groups,
                           form=form,
                           error=error,
                           success=success)


# question string edit
@app.route("/editQuestionString/<attribute_id>", methods=["GET"])
@login_required
def edit_question_view(attribute_id):
    attr = Attribute.query.get(attribute_id)
    json_a = json.loads(attr.attribute_question)

    return render_template("langTemplate.html", attribute=json_a, redirect_url=url_for('views.admin_view'),
                           post_url=url_for('views.edit_question_string', attribute_id=attr.id))


# question string edit post handler
@app.route("/edit_question_string/<attribute_id>", methods=["POST"])
@login_required
def edit_question_string(attribute_id):
    attr = Attribute.query.get(attribute_id)

    try:
        form = request.form
        jsoned = json.loads(attr.attribute_question)

        # Once the old data has been loaded, check that new data is not empty. If not empty, change the new data.
        for key in jsoned:
            if(len(form[key]) > 0):
                jsoned[key] = form[key]

        # Then save the new data into the attribute_question as json.
        attr.attribute_question = json.dumps(jsoned)
        db.session.commit()
    except:
        print('Data parsing gone goofed')

    return redirect(url_for("views.admin_view"))


# attribute name edit
@app.route("/editAttributeName/<attribute_id>", methods=["GET"])
@login_required
def edit_attribute_name_view(attribute_id):
    attr = Attribute.query.get(attribute_id)
    json_a = json.loads(attr.attribute_name)
    return render_template("langTemplate.html", attribute=json_a, redirect_url=url_for('views.admin_view'),
                           post_url=url_for('views.edit_attribute_name', attribute_id=attr.id))


# Attribute name edit post handler.
@app.route("/edit_attribute_name/<attribute_id>", methods=["POST"])
@login_required
def edit_attribute_name(attribute_id):
    attr = Attribute.query.get(attribute_id)

    try:
        form = request.form
        jsoned = json.loads(attr.attribute_name)

        # Once the old data has been loaded, check that new data is not empty. If not empty, change the new data.
        for key in jsoned:
            if(len(form[key]) > 0):
                jsoned[key] = form[key]

        # Then save the new data into the attribute_question as json.
        attr.attribute_name = json.dumps(jsoned)
        db.session.commit()
    except:
        print('Data parsing failed in attribute_name_edit')

    return redirect(url_for("views.admin_view"))


# Tooltip edit
@app.route("/editTooltip/<attribute_id>", methods=["GET"])
@login_required
def edit_tooltip_view(attribute_id):
    attr = Attribute.query.get(attribute_id)
    json_a = json.loads(attr.attribute_tooltip)
    return render_template("langTemplate.html", attribute=json_a, redirect_url=url_for('views.admin_view'),
                           post_url=url_for('views.edit_tooltip', attribute_id=attr.id))


# Tooltip edit post handler.
@app.route("/edit_tooltip/<attribute_id>", methods=["POST"])
@login_required
def edit_tooltip(attribute_id):
    attr = Attribute.query.get(attribute_id)

    try:
        form = request.form
        jsoned = json.loads(attr.attribute_tooltip)

        # Once the old data has been loaded, check that new data is not empty. If not empty, change the new data.
        for key in jsoned:
            if(len(form[key]) > 0):
                jsoned[key] = form[key]

        # Then save the new data into the attribute_tooltip as json.
        attr.attribute_tooltip = json.dumps(jsoned)
        db.session.commit()
    except:
        print('Data parsing failed in attribute_name_edit')

    return redirect(url_for("views.admin_view"))


# set activity status
@app.route("/de95b/<attribute_id>", methods=["POST"])
@login_required
def setActive(attribute_id):
    attr = Attribute.query.get(attribute_id)

    if attr.active:
        attr.active = False
    else:
        attr.active = True

    db.session.commit()
    return redirect(url_for("views.admin_view"))


# set group
@app.route("/gs59e/<attribute_id>", methods=["POST"])
@login_required
def setGroup(attribute_id):
    attr = Attribute.query.get(attribute_id)
    selected_group = request.form.get('select_group')
    grp = QuestionGroup.query.get(selected_group)
    try:
        if grp:
            if attr.grouping_id != grp.id:
                attr.grouping_id = grp.id
        else:
            attr.grouping_id = None

        db.session.commit()
    except:
        db.session.rollback()

    return redirect(url_for("views.admin_view"))


# Edit attribute probability
@app.route("/edit_attribute_probability/<attribute_id>", methods=["GET"])
@login_required
def edit_attribute_probability_view(attribute_id):
    attr = Attribute.query.get(attribute_id)
    string = attr.probability
    return render_template("singleStringEditTemplate.html", string=string, redirect_url=url_for('views.admin_view'),
                           post_url=url_for('views.edit_attribute_probability_float', attribute_id=attr.id))


# attribute probability handler
@app.route("/edit_attribute_probability/<attribute_id>", methods=["POST"])
@login_required
def edit_attribute_probability_float(attribute_id):
    attr = Attribute.query.get(attribute_id)

    try:
        form = request.form
        prob = attr.probability
        if len(form.get('string')) > 0:
            attr.probability = float(form.get('string'))
            db.session.commit()
    except:
        print('Data parsing failed in attribute_probability_edit')
        return redirect(url_for("views.edit_attribute_probability_view", attribute_id=attr.id, error="Edit failed, value has to be float"))

    return redirect(url_for("views.admin_view"))


def validate_localized_json(attribute_name, languages=('fi', 'sv', 'en')):
    def _validate(form, field):
        try:
            json_dict = json.loads(field.data)
        except:
            raise ValidationError(
                f'{attribute_name} needs to be JSON parseable string')

        for x in languages:
            if x not in json_dict or not isinstance(json_dict[x], str):
                raise ValidationError(
                    f'{attribute_name} must be defined for {languages}, at least {x} missing!')

    return _validate


class AttributeForm(FlaskForm):
    attribute_id = StringField('Attribute', [validators.Length(min=1, max=12)])
    attribute_name = StringField('Attribute name',
                                 validators=[validators.Length(min=1, max=1000),
                                             validate_localized_json('attribute_name')],
                                 default='{"fi": "Uusi attribuutti", "sv": "Ett nytt attribut", "en": "A new attribute"}')
    attribute_question = StringField('Question string',
                                     validators=[validators.Length(min=1, max=1000),
                                                 validate_localized_json('attribute_question')],
                                     default='{"fi": "Kysymys", "sv": "Frågan", "en": "The question"}')
    attribute_tooltip = StringField('Tooltip info',
                                    validators=[validators.Length(min=1, max=1000),
                                                validate_localized_json('attribute_tooltip')],
                                    default='{"fi":"", "sv":"", "en":""}')
    attribute_active = BooleanField('Active', default=False)
    attribute_group_id = SelectField(
        'Grouping id', choices=[('', 'Not grouped')])
    attribute_probability = DecimalField(
        'Probability', [validators.NumberRange(min=0.0, max=1.0)], default=0.0)

    def validate_attribute_id(form, field):
        if Attribute.query.filter_by(attribute_id=field.data).count() > 0:
            raise ValidationError(
                f'Attribute ID {field.data} is already in use!')

    def validate_attribute_group_id(form, field):
        if field.data != '' and QuestionGroup.query.filter_by(grouping_key=field.data).count() == 0:
            raise ValidationError(
                f'Attribute group id {field.data} not found!')


@app.route('/attribute/new', methods=['POST'])
@login_required
def add_attribute():
    groups = QuestionGroup.query.all()

    form = AttributeForm()
    form.attribute_group_id.choices += [
        (x.grouping_key, f'{x.grouping_key} - {x.group_name}') for x in groups]

    if form.validate_on_submit():
        group = form.attribute_group_id.data
        if group == '':
            group = None

        attribute = Attribute(id_=form.attribute_id.data,
                              name=form.attribute_name.data,
                              question=form.attribute_question.data,
                              tooltip=form.attribute_tooltip.data,
                              probability=form.attribute_probability.data,
                              active=form.attribute_active.data,
                              group=group)

        db.session.add(attribute)
        db.session.commit()

        building_classes = BuildingClass.query.all()
        class_attributes = []
        for x in building_classes:
            class_attributes.append(ClassAttribute(attribute, x, False))
        db.session.add_all(class_attributes)
        db.session.commit()

        return redirect(url_for('views.admin_view', success=f'Added attribute {form.attribute_id.data}'))
    else:
        print('Validation failed:', form.errors)
        return redirect(url_for('views.admin_view', error=f'Failed to add attribute: {form.errors}'))
