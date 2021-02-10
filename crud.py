from model import db, User, ProjectRecord, PatternLibrary, connect_to_db

def create_user(user_name, user_email, user_password):
    """Create and return a new user."""

    user = User(user_email=user_email, user_password=user_password, user_name=user_name)

    db.session.add(user)
    db.session.commit()

    return user

def create_project(project_name, swatch_width, 
                    swatch_height, project_width, 
                    project_height, current_row,  
                    current_index):
    """Create and return a new project."""

    project = ProjectRecord(
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

def create_pattern(pattern_name, pattern_description, pattern_instructions):
    """Create and return a new stitch pattern."""

    pattern = PatternLibrary(
                pattern_name=pattern_name,
                pattern_description=pattern_description,
                pattern_instructions=pattern_instructions)

    db.session.add(pattern)
    db.session.commit()

    return pattern

def get_patterns():
    """Return all patterns."""

    return PatternLibrary.query.all()

def get_projects():
    """Return all projects."""

    return ProjectRecord.query.all()

def get_users():
    """Return all users."""

    return User.query.all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()