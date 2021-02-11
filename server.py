
from flask import Flask, jsonify, render_template, request, flash, session, redirect
from model import connect_to_db, User, ProjectRecord, PatternLibrary
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Show the homepage."""

    return render_template('base.html')


if __name__ == '__main__':
    #connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)