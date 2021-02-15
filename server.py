
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

#TODO finish this route
@app.route('/api/instructions/<int:pattern_id>')
def instructions(pattern_id):
    """Access pattern instructions from database."""

    instructions = PatternLibrary.query.get(pattern_id)

    if instructions:
        return jsonify({'status': 'success',
                        'pattern_id': instructions.pattern_id,
                        'pattern_name': instructions.pattern_name, 
                        'pattern_instructions': instructions.pattern_instructions,
                        'pattern_description': instructions.pattern_description, 
                        'pattern_repeat_width': instructions.pattern_repeat_width,
                        'pattern_repeat_height': instructions.pattern_repeat_height})
    else:
        return jsonify({'status': 'error',
                        'message': 'Invalid input, please try again.'})


@app.route('/profile')
def profile_page():
    """View profile page."""

    return render_template('profile.html')

@app.route('/photos')
def photos_page():
    """View photos page."""

    return render_template('photos.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
