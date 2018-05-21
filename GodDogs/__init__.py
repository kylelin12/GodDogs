from flask import Flask, url_for, redirect, session, request, render_template
from utils import login
import sqlite3


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        redirect(url_for("index"))
    
    return render_template('index.html')

@app.route('/profile', methods=["GET", "POST"])
def about():
    return render_template('profile.html', "DANIEL")

if __name__ == '__main__':
    app.debug = True
    app.run()
