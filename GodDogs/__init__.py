from flask import Flask, url_for, redirect, session, request, render_template
#from utils import login
import sqlite3

from os import path

app = Flask(__name__)

DIR = path.dirname(__file__)

# Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        redirect(url_for('index'))
    return render_template('index.html')

# Global chatroom
@app.route('/gchat', methods=['GET', 'POST'])
def gchat():
    if request.method == 'POST':
        redirect(url_for('gchat'))
    return render_template('gchat.html')

# Shows your profile if from top right
# Shows any user's profile if their name is selected
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        redirect(url_for('profile'))
    return render_template('profile.html', name='DANIEL')

# Shows your list of friends if logged in
# If not logged in, redirect to login
@app.route('/friendslist', methods=['GET', 'POST'])
def friendslist():
    if request.method == 'POST':
        redirect(url_for('friendslist'))
    return render_template('friendslist.html', name='DANIEL')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        redirect(url_for('register'))
    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Delete session cookie etc.
    return redirect(url_for('index'))

@app.route('/authenticate', methods=['GET','POST'])
def authenticate():
    print "xd"
    user = request.form.get['email']
    pw = request.form.get["key"]

    print "[app] user is " + user
    print "[app] pw is " + pw

    if db.look_for(user):
        #authenticate pass
        print "hi"
        if db.check_pass(user, pw):
            session['user'] = user
            return redirect(url_for('root'))
        else:
            flash ("Incorrect Password.")
            return redirect(url_for('login'))
    else:
        flash ("User does not exist.")
        return redirect(url_for('login'))

@app.route('/user_creation', methods=['POST'])
def user_creation():
    print "xd"
    user = request.form['email']
    pw = request.form['key']
    pw_confirm = request.form['confirm']

    if db.look_for(user):
        flash ("User already exists")
        return redirect(url_for('register'))
    if pw != pw_confirm:
        flash ("Passwords must match")
        return redirect(url_for('register'))
    db.add_user(user, pw)
    flash ("Account Created")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = False
    app.run()
