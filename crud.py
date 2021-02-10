from model import db, User, ProjectRecord, PatternLibrary, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()