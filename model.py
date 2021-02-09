from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    user_password = db.Column(db.String(30), nullable=False)
    user_name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        """Show info about user."""

        return f"<User_id= {self.user_id} user_name= {self.user_name}>"


class ProjectRecord(db.Model):
    """Date model for a project record."""

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    pattern_id = 
    user_id =
    swatch_width = db.Column(db.Integer, nullable=False)
    swatch_height = db.Column(db.Integer, nullable=False)
    project_width = db.Column(db.Integer, nullable=False)
    project_height = db.Column(db.Integer, nullable=False)
    current_row = db.Column(db.Integer, nullable=False)
    current_index = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Project id= {self.project_id} Project name= {self.project_name}>"


class PatternLibrary(db.Model):
    """Data model for stitch patterns."""

    __tablename__ = "patterns"

    pattern_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pattern_name = db.Column(db.String(100), nullable=False)
    pattern_description = db.Column(db.String(), nullable=False)
    pattern_instructions = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Pattern id= {self.pattern_id} Patter name= {self.pattern_name}>"

# change name of postgres file to something for my project, then uncomment function
# def connect_to_db(app):
#     """Connect the database to our Flask app."""

#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///animals'
#     app.config['SQLALCHEMY_ECHO'] = False
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.app = app
#     db.init_app(app)        

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    print('Connected to db!')


#add foreign keys
#add relationships