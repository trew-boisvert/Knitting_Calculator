from model import db, User, ProjectRecord, Pattern, Instruction, Post, connect_to_db
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
        Each pattern will need multiple instruction rows."""

    instruction = Instruction(
                    pattern_id=pattern_id,
                    instruction_row=instruction_row,
                    instruction_text=instruction_text)

    db.session.add(instruction)
    db.session.commit()

    return instruction

def create_post(user_id, post_date, post_title, post_comment, post_photo_link):
    """Create and return a new post."""

    post = Post(
        user_id=user_id,
        post_date=post_date,
        post_title=post_title,
        post_comment=post_comment,
        post_photo_link=post_photo_link)

    db.session.add(post)
    db.session.commit()

    return post

def save_progress(projectID, current_row, current_index):
    """Save changes in current row and current index to project record in database."""

    project = ProjectRecord.query.get(projectID)
    project.current_row = current_row
    project.current_index = current_index

    db.session.add(project)
    db.session.commit()

    return project

def delete_user_project(projectID):
    """Delete a project record from the database."""

    project = ProjectRecord.query.get(projectID)

    db.session.delete(project)
    db.session.commit()

    return

def delete_user(userID):
    """Delete a user from the database."""

    user = User.query.get(userID)

    db.session.delete(user)
    db.session.commit()

    return

def delete_all_projects_for_single_user(userID):
    """Delete all of the project records of a single user."""

    projects = ProjectRecord.query.filter(ProjectRecord.user_id == userID).all()

    for project in projects:
        db.session.delete(project)
            
    db.session.commit()

    return

def delete_all_posts_for_single_user(userID):
    """Delete all of the posts of a single user."""

    posts = Post.query.filter(Post.user_id == userID).all()

    for post in posts:
        db.session.delete(post)
        
    db.session.commit()

    return

def get_patterns():
    """Return all patterns."""

    return Pattern.query.all()

def get_projects():
    """Return all projects."""

    return ProjectRecord.query.all()

def get_posts():
    """Return all posts."""

    return Post.query.all()

def get_project_by_id(id):
    """Find a project record by project_id."""

    return ProjectRecord.query.filter(ProjectRecord.project_id == id).first()

def get_pattern_by_name(name):
    """Find a pattern by name."""
    
    return Pattern.query.filter(Pattern.pattern_name == name).first()

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