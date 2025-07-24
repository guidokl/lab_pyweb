import sqlite3
from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import url_for

DATABASE = './sqlite/users.db'

app = Flask(__name__)

# SQLITE connection
def get_db():
    """
    Returns a db connection for the current request.
    If no connection exists, it ccreates one and stores it in Flask's 'g' object
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

# Close DB connection after request
@app.teardown_appcontext
def close_db(error):
    """
    Closes the database connection at the end of the request
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

# index.html
@app.route("/")
def home():
    name = "guido"
    return render_template("index.html", name=name)

# register.html
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
        except sqlite3.IntegrityError:
            error = "Username already taken"
    return render_template('register.html', error=error)
        
# Main
if __name__ == "__main__":
    app.run(debug=True)