from flask import *
from utils import auth,database
import sqlite3
from werkzeug.utils import secure_filename
import time as time_

import os
UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def make_secret_key():
    return os.urandom(32)

app.secret_key = make_secret_key()

app.jinja_env.globals.update(logged_in = auth.logged_in)

DIR = os.path.dirname(__file__)
messages = database.get_global_message()

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
    if auth.logged_in():
        return render_template('gchat.html', messages=messages)
    else:
        session['alert-type'] = 'error'
        flash('Please log in before joining the global chat')
        return redirect(url_for('login'))

@app.route("/_receiveMessage", methods=["POST"])
def receiveMessage():
    message = request.form['chatText']
    name = session['username']
    if message.strip() != '':
        messages.append((name, message))
        database.add_global_message(name, message)
    return ('', 204)

@app.route("/_sendMessages")
def sendMessagesList():
    rendered = getHtml()
    return rendered

def getHtml():
    text = '''  {% for name, msg in messages|reverse %}
                    {% if loop.index0 % 2 == 0 %}
                        <div class="row message-bubble" style="background-color: #F5F5F5"> <p class="text-muted">{{ name }}</p> <p>{{ msg }}</p> </div> <br>
                    {% else %}
                        <div class="row message-bubble"> <p class="text-muted">{{ name }}</p> <p>{{ msg }}</p> </div> <br>
                    {% endif %}
                {% endfor %}'''
    return render_template_string(text, messages=messages)


# Shows your profile if from top right
# Shows any user's profile if their name is selected
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        redirect(url_for('profile'))
    if auth.logged_in():
        return render_template('profile.html', name='DANIEL')
    else:
        session['alert-type'] = 'error'
        flash('Please log in before checking your profile')
        return redirect(url_for('login'))

# Shows your list of friends if logged in
# If not logged in, redirect to login
@app.route('/friendslist', methods=['GET', 'POST'])
def friendslist():
    if request.method == 'POST':
        redirect(url_for('friendslist'))
    if auth.logged_in():
        return render_template('friendslist.html', name=session['username'])
    else:
        session['alert-type'] = 'error'
        flash('Please log in before checking your friends list')
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form['email']
        pw = request.form["key"]

        if auth.u_exists(user):
            if auth.login(user, pw):
                session['alert-type'] = 'success'
                flash('Welcome to Dogechat %s!'%(user))
                return redirect(url_for('index'))
            else:
                session['alert-type'] = 'error'
                flash('You entered an incorrect password.')
        else:
            session['alert-type'] = 'error'
            flash('That email address does not have a registered account.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['email']
        pw = request.form["key"]

        pw_ver = request.form['key-confirm']
        if (pw == pw_ver):
            if auth.new_user(user, pw):
                session['alert-type'] = 'success'
                flash('Your account has been successfully created. Please log in.')
                return redirect(url_for('login'))
            else:
                session['alert-type'] = 'error'
                flash('That email is already in use. Please use another one.')
        else:
            session['alert-type'] = 'error'
            flash('The passwords you entered do not match.')
            
    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Delete session cookie etc.
    if auth.logged_in():
        auth.logout()
        session['alert-type'] = 'notice'
        flash('You have been logged out.')
    else:
        session['alert-type'] = 'error'
        flash('You can\'t log out if you aren\'t logged in.')
    return redirect(url_for('index'))

@app.route('/storePicData', methods=['POST'])
def storePicData():
	#print 'xd'
	#print request.form['data']
	#print request.form['targetUserArray']
	print session['username']
        print request.form['targetUserArray']
        userList = request.form['targetUserArray'].split(",")
        for receiver in userList:
            database.add_picture(session['username'],receiver,request.form['data'],int(round(time_.time()*1000)))
	return "pics Processed"

if __name__ == '__main__':
    app.debug = False
    app.run()
