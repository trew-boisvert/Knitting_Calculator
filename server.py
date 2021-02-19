
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

def get_instruction_array(list_of_objects):
    result = []
    for line in list_of_objects:
        result.append(line.instruction_text)
    return result

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

    stitchChoice = Pattern.query.get(pat_ID)
    all_instructions_table = Instruction.query.filter(Instruction.pattern_id == pat_ID).order_by(Instruction.instruction_row).all()
    stitchInstructions = get_instruction_array(all_instructions_table)
    print(stitchInstructions)
    #select instruction_text from instructions where pattern_id=2 order by instruction_row;
    cast_on = calculate_width(sWidth, pWidth, stitchChoice.pattern_repeat_width)
    row_total = calculate_height(sHeight, pHeight, stitchChoice.pattern_repeat_height)

    if stitchChoice:
        return jsonify({'status': 'success',
                        'pattern_id': stitchChoice.pattern_id,
                        'pattern_name': stitchChoice.pattern_name, 
                        'pattern_description': stitchChoice.pattern_description, 
                        'pattern_repeat_width': stitchChoice.pattern_repeat_width,
                        'pattern_repeat_height': stitchChoice.pattern_repeat_height, 
                        'cast_on': cast_on,
                        'row_total': row_total,
                        'stitch': stitchInstructions,
                        'start': f'To start, cast on {cast_on} stitches.'})
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
