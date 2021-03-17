# Knitting_Calculator

## Table of Contents

* [Summary](#summary)
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#setup)
* [About the Developer](#developer)

## <a name="summary"></a>Summary
**Knittr** is a calculator for knitters that performs project calculations for them.  It takes in input about a user's stitch pattern choice, swatch measurements, and desired finished size for a blanket, scarf, or shawl, and then calculates and generates a custom knitting pattern for the user to follow.  

## <a name="tech-stack"></a>Tech Stack
__Front End:__ HTML5, Jinja2, CSS, JavaScript, AJAX, jQuery, Bootstrap<br/>
__Back End:__ Python, Flask, PostgreSQL, SQLAlchemy <br/>

## <a name="features"></a>Features

Create and Log in to an account.

![Login GIF](/static/images/LoginGIF.gif)

Use knitting calculator to generate a custom knitting pattern and save it to your profile.  Iterate through the pattern line by line while your progress is automatically saved.  

Author your own stitch pattern and add it to the database using the Custom Stitch adder.

Upload photos of your knitting projects to the photo/discussion board.

Log out from or delete your account.  Knittr respects your right to be forgotten!

## <a name="setup"></a>Setup/Installation

#### Requirements:

- Python 3.6.8
- PostgreSQL

To run this app on your local computer, follow these steps:

Clone repository:
```
$ git clone https://github.com/trew-boisvert/Knitting_Calculator.git
```

Create a virtual environment:
```
$ virtualenv env
```

Activate the virtual environment:
```
$ source env/bin/activate
```

Install dependencies:
```
$ pip3 install -r requirements.txt
```

To run Flask you need to set a secret key. Create a 'secrets.sh' file in the project directory and add a key.

Add the key to your environmental variables (do this each time you restart your virtual environment):
```
$ source secrets.sh
```

Create database 'knitting':
```
$ createdb knitting
```

Create your database tables:
```
$ python3 model.py
```

Seed database with data (optional):
```
$ python3 seed_database.py
```

Run app from the command line:
```
$ python3 server.py
```

Visit localhost:5000 on your browser.

## <a name="developer"></a>About the Developer

Trew Boisvert (they/them) has a background in fashion and textiles.  They enjoy solving puzzles, be it the logic puzzles inherent in programming, or the mathmatical puzzle of creating clothing patterns.  You can learn more about them on their <a href="https://www.linkedin.com/in/trew-boisvert-a78309a1/">LinkedIn.</a>
