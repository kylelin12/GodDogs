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

if __name__ == '__main__':
    app.debug = False
    app.run()
