from model import db, User, ProjectRecord, Pattern, Instruction, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(user_name, user_email, user_password):
    """Create and return a new user."""

    user = User(user_email=user_email, user_password=generate_password_hash(user_password, method='sha256'), user_name=user_name)

    db.session.add(user)
    db.session.commit()

    return user

def create_project(user_id, pattern_id, project_name, swatch_width, 
                    swatch_height, project_width, 
                    project_height, current_row,  
                    current_index):
    """Create and return a new project."""

    project = ProjectRecord(
                user_id=user_id, 
                pattern_id=pattern_id, 
                project_name=project_name,
                swatch_width=swatch_width,
                swatch_height=swatch_height,
                project_width=project_width,
                project_height=project_height,
                current_row=current_row,
                current_index=current_index)
    
    db.session.add(project)
    db.session.commit()

    return project

def create_pattern(pattern_name, pattern_description, 
                    pattern_repeat_width, 
                    pattern_repeat_height):
    """Create and return a new stitch pattern."""

    pattern = Pattern(
                pattern_name=pattern_name,
                pattern_description=pattern_description,
                pattern_repeat_width=pattern_repeat_width,
                pattern_repeat_height=pattern_repeat_height)

    db.session.add(pattern)
    db.session.commit()

    return pattern

def create_instruction(pattern_id, instruction_row, instruction_text):
    """Create and return a new stitch instruction row.
        Each pattern will need multiple rows."""

    instruction = Instruction(
                    pattern_id=pattern_id,
                    instruction_row=instruction_row,
                    instruction_text=instruction_text)

    db.session.add(instruction)
    db.session.commit()

    return instruction

def save_progress(projectID, current_row, current_index):
    """Save changes in current row and current index to project record in database."""

    project = ProjectRecord.query.get(projectID)
    project.current_row = current_row
    project.current_index = current_index

    db.session.add(project)
    db.session.commit()

    return project

def get_patterns():
    """Return all patterns."""

    return Pattern.query.all()

def get_projects():
    """Return all projects."""

    return ProjectRecord.query.all()

def get_project_by_id(id):
    """Find a project record by project_id."""
    return ProjectRecord.query.filter(ProjectRecord.project_id == id).first()

def get_users():
    """Return all users."""

    return User.query.all()

def find_user_by_email(email):
    """Find a user by their email address."""

    return User.query.filter(User.user_email == email).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()