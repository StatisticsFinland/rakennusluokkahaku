from flask import escape, request
from . import views as app


@app.route("/")
def index():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)}"
