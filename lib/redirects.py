from app import flask_app
from flask import redirect

@flask_app.route("/")
def main():
    return redirect("/sessions")
