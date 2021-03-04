from flask import Flask, jsonify, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, User, ProjectRecord, Pattern, Instruction
import crud
from jinja2 import StrictUndefined
from werkzeug.security import generate_password_hash, check_password_hash
# can do crud.check_password_hash as a refactor, and remove above line

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

def get_project_object(list_of_objects):
    result = {}
    for obj in list_of_objects:
        result[obj.project_id] = obj.project_name
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

@app.route('/logout')
def logout_page():
    """View logout page."""

    if session['logged_in'] == True:
        return render_template('logout.html')
    else:
        flash('You are not logged in.')
        return redirect('/login')

@app.route('/handle-login', methods=['POST'])
def handle_login():
    """Log the user into the application."""
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(user_email=email).first()

    if not user or not check_password_hash(user.user_password, password):
        flash('Incorrect email/password.  Please try again')
        return redirect('/login')
    session['logged_in'] = True
    session['user_id'] = user.user_id
    session.modified = True
    print(session)
    flash(f'Logged in as {user.user_name}')    
    return redirect('/profile')

@app.route('/handle-logout', methods=['POST'])
def handle_logout():
    """Log the user out of the application."""

    session['logged_in'] = False

    return jsonify({'message': 'Successfully logged out!'})    

@app.route('/new-account', methods=['POST'])
def create_new_user():
    """Create/register a new user."""

    email = request.form.get('newemail')
    password = request.form.get('newpassword')
    username = request.form.get('newusername')

    user = crud.find_user_by_email(email)
    if user:
        flash('There is already an account with that email address.')
    else:
        crud.create_user(username, email, password)
        flash('Your account has been created!  Please log in.')

    return redirect('/login')

@app.route('/calculator')
def calculator_page():
    """View calculator page."""

    return render_template('calculator.html')


@app.route('/api/instructions', methods=['POST'])
def instructions():
    """Access pattern instructions from database, perform and return calculations."""

    pat_ID = int(request.form.get('patID'))
    sWidth = int(request.form.get('sWidth'))
    sHeight = int(request.form.get('sHeight'))
    pWidth = int(request.form.get('pWidth'))
    pHeight = int(request.form.get('pHeight'))
    pName = request.form.get('pName')

    stitchChoice = Pattern.query.get(pat_ID)
    all_instructions_table = Instruction.query.filter(Instruction.pattern_id == pat_ID).order_by(Instruction.instruction_row).all()
    stitchInstructions = get_instruction_array(all_instructions_table)
    
    cast_on = calculate_width(sWidth, pWidth, stitchChoice.pattern_repeat_width)
    row_total = calculate_height(sHeight, pHeight, stitchChoice.pattern_repeat_height)

    session['pattern_id'] = pat_ID
    session['swatch_width'] = sWidth
    session['swatch_height'] = sHeight
    session['project_width'] = pWidth
    session['project_height'] = pHeight
    session['cast_on'] = cast_on
    session['row_total'] = row_total
    session['stitchInstructions'] = stitchInstructions
    session['project_name'] = pName
    session.modified = True

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

@app.route('/save_pattern', methods=['POST'])
def save_pattern():
    """Save an in-progress pattern to user profile."""
    currentRow = int(request.form.get('currentRow'))
    currentIndex = int(request.form.get('currentIndex'))

    session['currentRow'] = currentRow
    session['currentIndex'] = currentIndex
    session.modified = True

    crud.create_project(session['user_id'], session['pattern_id'], session['project_name'], session['swatch_width'], 
                    session['swatch_height'], session['project_width'], 
                    session['project_height'], session['currentRow'],  
                    session['currentIndex'])

    return jsonify({'message': 'Project record saved!'})

@app.route('/profile')
def profile_page():
    """View profile page."""

    if session['logged_in'] == True:
        return render_template('profile.html')
    else:
        return redirect('/login')

@app.route('/api/projects', methods=['POST'])
def list_projects():
    """Retrieve and return project records associated with user."""
    all_user_projects = ProjectRecord.query.filter(ProjectRecord.user_id == session['user_id']).all()
    response = get_project_object(all_user_projects)
    return jsonify(response)

@app.route('/delete/<project_id>', methods=['POST', 'GET'])
def ask_if_delete_project(project_id):
    """Show delete page for a selected project record."""

    project = crud.get_project_by_id(project_id)
    session['to_delete'] = project.project_id
    session.modified = True

    return render_template('delete.html', project=project)

@app.route('/api/delete', methods=['POST'])
def delete_project():
    """Delete selected user project from database."""

    crud.delete_user_project(session['to_delete'])

    return jsonify({'message': 'Project record destroyed!'})

@app.route('/api/accountdelete', methods=['POST'])
def delete_user_account():
    """Delete user account and related project records from database."""

    crud.delete_all_projects_for_single_user(session['user_id'])
    crud.delete_user(session['user_id'])
    session['logged_in'] = False

    return jsonify({'message': 'Account destroyed!'})

@app.route('/projectcontinue/<project_id>', methods=['POST', 'GET'])
def continue_knitting(project_id):
    """View Continue-Knitting page."""

    project = crud.get_project_by_id(project_id)

    session['project_id'] = project.project_id
    session['project_name'] = project.project_name
    session['pattern_id'] = project.pattern_id
    session['swatch_width'] = project.swatch_width
    session['swatch_height'] = project.swatch_height
    session['project_width'] = project.project_width
    session['project_height'] = project.project_height
    session['currentRow'] = project.current_row
    session['currentIndex'] = project.current_index

    stitchChoice = Pattern.query.get(project.pattern_id)
    all_instructions_table = Instruction.query.filter(Instruction.pattern_id == project.pattern_id).order_by(Instruction.instruction_row).all()
    stitchInstructions = get_instruction_array(all_instructions_table)
    cast_on = calculate_width(project.swatch_width, project.project_width, stitchChoice.pattern_repeat_width)
    row_total = calculate_height(project.swatch_height, project.project_height, stitchChoice.pattern_repeat_height)
    
    session['cast_on'] = cast_on
    session['row_total'] = row_total
    session['stitchInstructions'] = stitchInstructions
    session.modified = True
    print(session)

    return render_template('projectcontinue.html', project=project)

@app.route('/api/projectcontinue', methods=['POST'])
def load_progress_to_calculator():
    """Calculate and return values needed to continue project from last save point."""
    
    return jsonify({'cast_on': session['cast_on'],
                    'row_total': session['row_total'],
                    'stitch': session['stitchInstructions'],
                    'currentRow': session['currentRow'], 
                    'currentIndex': session['currentIndex']})

@app.route('/api/savecontinue', methods=['POST'])
def savecontinue():
    """Save progress from Continue Calculator on Next/Prev button click."""
    currentRow = int(request.form.get('currentRow'))
    currentIndex = int(request.form.get('currentIndex'))

    session['currentRow'] = currentRow
    session['currentIndex'] = currentIndex
    session.modified = True

    crud.save_progress(session['project_id'], currentRow, currentIndex)

    return jsonify({'message': 'Project record saved!'})    

@app.route('/photos')
def photos_page():
    """View photos page."""

    return render_template('photos.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)



