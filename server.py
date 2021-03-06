from flask import Flask, jsonify, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, User, ProjectRecord, Pattern, Instruction, Post
import crud
import functions
from datetime import datetime
from jinja2 import StrictUndefined
import cloudinary as Cloud
import cloudinary.uploader
import cloudinary.api
from APIconfig import APIsecret, SecretKey

app = Flask(__name__)
app.secret_key = SecretKey
app.jinja_env.undefined = StrictUndefined

cloudinary.config( 
  cloud_name = "knittr", 
  api_key = "163782255322919", 
  api_secret =  APIsecret
)

#Welcome####################################################################################################

@app.route('/')
def welcome_page():
    """Show the welcome/homepage."""

    return render_template('welcome.html')

#Login/Signup##########################################################################################

@app.route('/login')
def login_page():
    """View login page."""

    return render_template('login.html')

@app.route('/handle-login', methods=['POST'])
def handle_login():
    """Log the user into the application."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(user_email=email).first()

    if not user or not crud.check_password_hash(user.user_password, password):
        flash('Incorrect email/password.  Please try again')
        return redirect('/login')

    session['logged_in'] = True
    session['user_id'] = user.user_id
    session.modified = True
    
    flash(f'Logged in as {user.user_name}')    
    return redirect('/profile')

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

#Calculator############################################################################################

@app.route('/calculator')
def calculator_page():
    """View calculator page."""

    if session['logged_in'] == False:
        flash('Please login or create account.')
        return render_template('login.html')

    patterns = crud.get_patterns()

    return render_template('calculator.html', patterns=patterns)

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
    stitchInstructions = functions.get_instruction_array(all_instructions_table)
    
    cast_on = functions.calculate_width(sWidth, pWidth, stitchChoice.pattern_repeat_width)
    row_total = functions.calculate_height(sHeight, pHeight, stitchChoice.pattern_repeat_height)

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

    crud.create_project(session['user_id'], 
                        session['pattern_id'], 
                        session['project_name'], 
                        session['swatch_width'], 
                        session['swatch_height'], 
                        session['project_width'], 
                        session['project_height'], 
                        session['currentRow'],  
                        session['currentIndex'])

    return jsonify({'message': 'Project record saved!'})

@app.route('/projectcontinue/<project_id>', methods=['POST', 'GET'])
def continue_knitting(project_id):
    """View Continue-Knitting page."""

    if session['logged_in'] == False:
        flash('Please login or create account.')
        return render_template('login.html')

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
    stitchInstructions = functions.get_instruction_array(all_instructions_table)
    cast_on = functions.calculate_width(project.swatch_width, project.project_width, stitchChoice.pattern_repeat_width)
    row_total = functions.calculate_height(project.swatch_height, project.project_height, stitchChoice.pattern_repeat_height)
    
    session['cast_on'] = cast_on
    session['row_total'] = row_total
    session['stitchInstructions'] = stitchInstructions
    session.modified = True

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

#Custom Stitch############################################################################################

@app.route('/customstitch')
def custom_stitch_page():
    """View custom stitch page."""
    
    if session['logged_in'] == False:
        flash('Please login or create account.')
        return render_template('login.html')

    return render_template('customstitch.html')

@app.route('/api/customstitch', methods=['POST'])
def custom_stitch_page_save():
    """Save custom stitch pattern."""

    stitchName = request.form.get('stitch-name')
    stitchDescription = request.form.get('stitch-description')
    stitchRepeatWidth = request.form.get('stitch-repeat-width')
    stitchRepeatHeight = request.form.get('stitch-repeat-height')
    stitchInstructionsList = request.form.getlist('stitch-instructions-list')

    new_pattern = crud.get_pattern_by_name(stitchName)

    if new_pattern:
        flash('A pattern by this name already exists.')
    else:
        new_pattern = crud.create_pattern(stitchName, stitchDescription, stitchRepeatWidth, stitchRepeatHeight)
        
        for index in range(len(stitchInstructionsList)):
            crud.create_instruction(new_pattern.pattern_id, (index + 1), stitchInstructionsList[index])
        
        flash('New stitch pattern saved!')
    return redirect('/customstitch')

#Photos###################################################################################################

@app.route('/photos')
def photos_page():
    """View photos page."""

    if session['logged_in'] == False:
        flash('Please login or create account.')
        return render_template('login.html')

    posts = crud.get_posts()

    return render_template('photos.html', posts=posts)

@app.route('/api/photos', methods=["POST"])
def upload_photo_post():
    """Upload a photo post."""

    post_title = request.form.get('post_title')
    post_comment = request.form.get('post_comment')
    img_url = request.form.get('img_url')

    now = datetime.now()

    post = crud.create_post(session['user_id'], now, post_title, post_comment, img_url)

    return jsonify({'status': 'ok'})

#Profile###################################################################################################

@app.route('/profile')
def profile_page():
    """View profile page."""

    if session['logged_in'] == True:
        user = User.query.filter_by(user_id=session['user_id']).first()
        return render_template('profile.html', user=user)
    
    flash('You must be logged in to see profile.')
    return redirect('/login')

@app.route('/api/projects', methods=['POST'])
def list_projects():
    """Retrieve and return project records associated with user."""

    all_user_projects = ProjectRecord.query.filter(ProjectRecord.user_id == session['user_id']).all()
    
    return jsonify(functions.get_project_object(all_user_projects))

@app.route('/delete/<project_id>', methods=['POST', 'GET'])
def ask_if_delete_project(project_id):
    """Show delete page for a selected project record."""

    if session['logged_in'] == False:
        flash('Please login or create account.')
        return render_template('login.html')

    project = crud.get_project_by_id(project_id)
    session['to_delete'] = project.project_id
    session.modified = True

    return render_template('delete.html', project=project)

@app.route('/api/delete', methods=['POST'])
def delete_project():
    """Delete selected user project from database."""

    crud.delete_user_project(session['to_delete'])

    return jsonify({'message': 'Project record destroyed!'})

#Logout###################################################################################################

@app.route('/logout')
def logout_page():
    """View logout page."""

    if session['logged_in'] == True:
        return render_template('logout.html')
    
    flash('You are not logged in.')
    return redirect('/login')

@app.route('/handle-logout', methods=['POST'])
def handle_logout():
    """Log the user out of the application."""

    session['logged_in'] = False
    session.modified = True

    return jsonify({'message': 'Successfully logged out!'}) 

@app.route('/api/accountdelete', methods=['POST'])
def delete_user_account():
    """Delete user account and related project records and posts from database."""

    crud.delete_all_projects_for_single_user(session['user_id'])
    crud.delete_all_posts_for_single_user(session['user_id'])
    crud.delete_user(session['user_id'])
    session['logged_in'] = False
    session.modified = True

    return jsonify({'message': 'Account destroyed!'})



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
