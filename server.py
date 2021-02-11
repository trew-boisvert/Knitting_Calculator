
from flask import Flask, jsonify, render_template, request, flash, session, redirect
from model import connect_to_db, User, ProjectRecord, PatternLibrary
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def welcome_page():
    """Show the welcome/homepage."""

    return render_template('welcome.html')

@app.route('/login')
def login_page():
    """View login page."""

    return render_template('login.html')

@app.route('/calculator')
def calculator_page():
    """View calculator page."""

    return render_template('calculator.html')

@app.route('/profile')
def profile_page():
    """View profile page."""

    return render_template('profile.html')

@app.route('/photos')
def photos_page():
    """View photos page."""

    return render_template('photos.html')


if __name__ == '__main__':
    #connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)