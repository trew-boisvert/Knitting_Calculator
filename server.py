
from flask import Flask, jsonify, render_template, request, flash, session, redirect
from model import connect_to_db, User, ProjectRecord, Pattern, Instruction
import crud
from jinja2 import StrictUndefined



app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Functions for backend calculations

def calculate_width(swatch_width, project_width, repeat_size):
    """Calculate number of stitches for knitting project width."""
    stitches = 0
    width = 0
    while width < project_width:
        stitches += repeat_size
        width += swatch_width
    return stitches

def calculate_height(swatch_height, project_height, repeat_size):
    rows = 0
    height = 0
    while height < project_height:
        rows += repeat_size
        height += swatch_height
    return rows

#Routes

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
@app.route('/api/instructions', methods=['POST'])
def instructions():
    """Access pattern instructions from database, perform and return calculations."""

    pat_ID = int(request.form.get('patID'))
    sWidth = int(request.form.get('sWidth'))
    sHeight = int(request.form.get('sHeight'))
    pWidth = int(request.form.get('pWidth'))
    pHeight = int(request.form.get('pHeight'))
    #maybe don't call it 'instructions' now that that's a tablename in the database
    instructions = Pattern.query.get(pat_ID)
    # print(instructions.pattern_instructions[0])
    cast_on = calculate_width(sWidth, pWidth, instructions.pattern_repeat_width)
    row_total = calculate_height(sHeight, pHeight, instructions.pattern_repeat_height)
    if instructions:
        return jsonify({'status': 'success',
                        'pattern_id': instructions.pattern_id,
                        'pattern_name': instructions.pattern_name, 
                        'pattern_description': instructions.pattern_description, 
                        'pattern_repeat_width': instructions.pattern_repeat_width,
                        'pattern_repeat_height': instructions.pattern_repeat_height, 
                        'cast_on': cast_on,
                        'row_total': row_total})
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
