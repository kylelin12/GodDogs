from flask import Flask, url_for, redirect, session, request, render_template
from utils import auth
import sqlite3

import os

app = Flask(__name__)

def make_secret_key():
    return os.urandom(32)

app.secret_key = make_secret_key()

DIR = os.path.dirname(__file__)

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
    print "xd"
    if request.method == "POST":
        user = request.form['email']
        pw = request.form["key"]

        print "[app] user is " + user
        print "[app] pw is " + pw

        if auth.u_exists(user):
            if auth.login(user, pw):
                return redirect('index')
            else:
                print "bad pw"
                # bad pw
        else:
            print "bad user"
            #user doesn't exist
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['email']
        pw = request.form["key"]

        print "[app] user is " + user
        print "[app] pw is " + pw

        pw_ver = request.form['key-confirm']
        if (pw == pw_ver):
            if auth.new_user(user, pw):
                # Successfully created
                return redirect('login')
            else:
                print "user in use"
                # Registration error username in use
        else:
            print "bad pw"
            # PW do not match
            
    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Delete session cookie etc.
    if auth.logged_in():
        auth.logout()
        print "logged out"
        # You've been logged out
    else:
        print "not logged in"
        # Error not logged in
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = False
    app.run()
