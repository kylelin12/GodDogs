from flask import Flask, url_for, redirect, session, request, render_template, flash
from utils import auth,database
import sqlite3
import time as time_

import os

app = Flask(__name__)

app.secret_key = os.urandom(32)

app.jinja_env.globals.update(logged_in = auth.logged_in)

DIR = os.path.dirname(__file__)

# Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('index.html')

# Global chatroom
@app.route('/gchat', methods=['GET', 'POST'])
def gchat():
    if request.method == 'POST':
        return redirect(url_for('gchat'))
    if auth.logged_in():
        return render_template('gchat.html')
    else:
        session['alert-type'] = 'error'
        flash('Please log in before joining the global chat')
        return redirect(url_for('login'))

# Shows your profile if from top right
# Shows any user's profile if their name is selected
@app.route('/profile/<name>', methods=['GET', 'POST'])
def profile(name):
    if request.method == 'POST':
        return redirect(url_for('profile', name=name))
    if auth.logged_in():
        if auth.u_exists(name):
            bio = "TESTBIO"
            status = database.f_getstatus(session['username'], name)
            return render_template('profile.html', name=name, status=status, bio=bio)
        else:
            return render_template('noprofile.html')
    else:
        session['alert-type'] = 'error'
        flash('Please log in before checking your profile')
        return redirect(url_for('login'))

# Shows your list of friends if logged in
# If not logged in, redirect to login
@app.route('/friendslist', methods=['GET', 'POST'])
def friendslist():
    if request.method == 'POST':
        return redirect(url_for('friendslist'))
    if auth.logged_in():
        f_list = database.f_getlist(session['username'])
        return render_template('friendslist.html', f_list=f_list)
    else:
        session['alert-type'] = 'error'
        flash('Please log in before checking your friends list')
        return redirect(url_for('login'))

@app.route('/addfriend', methods=['GET', 'POST'])
def addfriend():
    friend = request.args.get('name')
    result = database.add_friendship(session['username'], friend)
    if result == True:
        session['alert-type'] = 'success'
        flash('You\'ve successfully added %s to your friends list'%(friend))
    else:
        session['alert-type'] = 'error'
        flash('An error occured when trying to add %s to your friends list'%(friend))
    return redirect(url_for('friendslist'))

@app.route('/removefriend', methods=['GET','POST'])
def removefriend():
    friend = request.args.get('name')
    result = database.remove_friendship(session['username'], friend)
    if result == True:
        session['alert-type'] = 'success'
        flash('You\'ve succcessfully removed %s from your friends list'%(friend))
    else:
        session['alert-type'] = 'error'
        flash('An error occured when trying to remove %s from your friends list'%(friend))
    return redirect(url_for('friendslist'))

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
@app.route("/messenger", methods=['GET','POST'])
def messenger():
	if request.method == 'POST':
        	return redirect(url_for('messenger'))
	if auth.logged_in():
		fList = database.f_getlist(session['username'])
		print fList
		return render_template("messenger.html", username=session['username'])
	else:
        	session['alert-type'] = 'error'
        	flash('Please log in before checking your messages')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = False
    app.run()
