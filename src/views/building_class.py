import json
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from . import views as app
from ..models import db, Attribute, BuildingClass, ClassAttribute


# Building classes view
@app.route("/801fc3c", methods=["GET"])
@login_required
def classes_view():
    b_class = vars(db.session.query(BuildingClass).first())
    b_class.pop("_sa_instance_state", None)
    b_class.pop("id", None)
    building_classes = BuildingClass.query.all()
    for one in building_classes:
        one.class_name = json.loads(one.class_name)["fi"]
    return render_template("classesView.html", building_classes=building_classes, object=b_class,
                           post_url=url_for('views.create_building_class'),
                           info='Only add building classes that are defined in Statistics Finland API.')

# Building class create post handler
@app.route("/create_building_class", methods=["POST"])
@login_required
def create_building_class():
    form = request.form
    if (not form["class_id"] or not form["class_name"]):
        flash("Fill all the fields.")
        return redirect(url_for("views.classes_view"))
    try:
        name = f'{{"fi":"{form["class_name"]}", "en":"[English]{form["class_name"]}", "sv":"[Svenska]{form["class_name"]}"}}'
        b_class = BuildingClass(class_id=form["class_id"],
                                class_name=name,
                                class_probability=form["class_probability"])
        db.session.add(b_class)
        db.session.commit()
        b_class = BuildingClass.query.filter_by(
            class_id=b_class.class_id).first()
        attributes = Attribute.query.all()
        for one in attributes:
            db.session.add(ClassAttribute(
                attribute=one, building_class=b_class))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Building class with corresponding class id already exists.")
        return redirect(url_for("views.classes_view"))
    except:
        flash("Probability should be a numeric value.")
        return redirect(url_for("views.classes_view"))

    return redirect(url_for("views.classes_view"))


# Class probability edit post handler.
@app.route("/edit_class_probability/<class_id>", methods=["POST"])
@login_required
def edit_class_probability(class_id):
    b_class = BuildingClass.query.get(class_id)
    try:
        b_class.class_probability = request.form["probability"]
        db.session.commit()
    except:
        db.session.rollback()
        flash("Probability should be a numeric value.")

    return redirect(url_for("views.classes_view"))


# Toggler for class having attribute
@app.route("/toggle_link_between_class_attribute/<class_attribute_id>", methods=["POST"])
@login_required
def toggle_link_between_class_attribute(class_attribute_id):
    link = ClassAttribute.query.get(class_attribute_id)

    if link.class_has_attribute:
        link.class_has_attribute = False
    else:
        link.class_has_attribute = True

    db.session.commit()
    return redirect(url_for("views.link_bclass_attribute_view", class_id=link.buildingclass_id))


# Edit class attribute probability
@app.route("/link_bclass_attribute_view/<class_id>", methods=["GET"])
@login_required
def link_bclass_attribute_view(class_id):
    bclass = BuildingClass.query.get(class_id)
    links = ClassAttribute.query.filter_by(buildingclass_id=class_id)

    bclass.class_name = json.loads(bclass.class_name)["fi"]
    for one in links:
        one.attribute.attribute_name = json.loads(
            one.attribute.attribute_name)["fi"]

    return render_template("bclass_attr_link.html", bclass=bclass, links=links)


# Class attribute probability edit post handler.
@app.route("/edit_class_attribute_probability/<class_attribute_id>", methods=["POST"])
@login_required
def edit_class_attribute_probability(class_attribute_id):
    link = ClassAttribute.query.get(class_attribute_id)

    try:
        link.custom_probability = request.form["probability"]
        db.session.commit()
    except:
        db.session.rollback()
        flash("Probability should be a numeric value.")

    return redirect(url_for("views.link_bclass_attribute_view", class_id=link.buildingclass_id))
