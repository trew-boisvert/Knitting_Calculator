
from flask import Flask, jsonify, render_template
#from model import connect_to_db, User, ProjectRecord, PatternLibrary



app = Flask(__name__)

@app.route('/')
def homepage():
    """Show the homepage."""

    return render_template('base.html')


if __name__ == '__main__':
    #connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)