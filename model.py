from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta

db = SQLAlchemy()


class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)

    user_project = db.relationship('ProjectRecord')
    post = db.relationship('Post')

    def __repr__(self):
        """Show info about user."""

        return f"<User_id= {self.user_id} user_name= {self.user_name}>"


class ProjectRecord(db.Model):
    """Date model for a project record."""

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    pattern_id = db.Column(db.Integer, db.ForeignKey('patterns.pattern_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    swatch_width = db.Column(db.Float, nullable=False)
    swatch_height = db.Column(db.Float, nullable=False)
    project_width = db.Column(db.Float, nullable=False)
    project_height = db.Column(db.Float, nullable=False)
    current_row = db.Column(db.Integer, nullable=False)
    current_index = db.Column(db.Integer, nullable=False)

    user = db.relationship('User')
    pattern = db.relationship('Pattern')

    def __repr__(self):
        return f"<Project id= {self.project_id} Project name= {self.project_name}>"


class Pattern(db.Model):
    """Data model for stitch patterns."""

    __tablename__ = "patterns"

    pattern_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pattern_name = db.Column(db.String(100), nullable=False)
    pattern_description = db.Column(db.String(), nullable=False)
    pattern_repeat_width = db.Column(db.Integer, nullable=False)
    pattern_repeat_height = db.Column(db.Integer, nullable=False)

    project = db.relationship('ProjectRecord')
    instruction = db.relationship('Instruction')

    def __repr__(self):
        return f"<Pattern id= {self.pattern_id} Pattern name= {self.pattern_name}>"

class Instruction(db.Model):
    """Data model for stitch pattern instructions."""

    __tablename__ = "instructions"

    instruction_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pattern_id = db.Column(db.Integer, db.ForeignKey('patterns.pattern_id'), nullable=False)
    instruction_row = db.Column(db.Integer, nullable=False)
    instruction_text = db.Column(db.String(), nullable=False)

    pattern = db.relationship('Pattern')

    def __repr__(self):
        return f"<Pattern id= {self.pattern_id} Instructions>"

class Post(db.Model):
    """Data model for posts to discussion board."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_date = db.Column(db.DateTime, nullable=False)
    post_title = db.Column(db.String(), nullable=False)
    post_comment = db.Column(db.String(), nullable=True)
    post_photo_link = db.Column(db.String(), nullable=False)

    user = db.relationship('User')

    def __repr__(self):
        return f"<Post id= {self.post_id}>"

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///knitting'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)        

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()
    print('Connected to db!')

