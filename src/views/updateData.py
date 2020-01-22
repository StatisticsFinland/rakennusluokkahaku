from flask import request
from flask_login import login_required
from . import views as app
from .. import building_data, classifier


@app.route("/update", methods=["GET"])
@login_required
def update():
    try:
        building_data.load_from_db()
        print("building data reloaded")
        classifier.load_from_db()
        print("classifier reloaded")
    except:
        print("updating failed")

    return ('', 204)
