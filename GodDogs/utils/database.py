import sqlite3

db = sqlite3.connect("GodDog.db")
c = db.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL);')
c.execute('CREATE TABLE IF NOT EXISTS pictures (sender TEXT, receiver TEXT, picture64 BLOB, time INT);')
c.execute('CREATE TABLE IF NOT EXISTS messages (sender TEXT, receiver TEXT, message TEXT, time INT);')
c.execute('CREATE TABLE IF NOT EXISTS globalchat (sender TEXT, message TEXT, time INT);')
c.execute('CREATE TABLE IF NOT EXISTS friendslist (id INT PRIMARY KEY, user1 TEXT NOT NULL, user2 TEXT NOT NULL, status INT NOT NULL)')
db.commit()
db.close()

# users Database

def add_user(u, p):
    f = "GodDog.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    if empty_db():
        c.execute('INSERT INTO users VALUES("%s", "%s");' %(u, p))
        db.commit()
        db.close()
        return True
    if check_pass(u) is None:
        c.execute('INSERT INTO users VALUES("%s", "%s");' %(u, p))
        db.commit()
        db.close()
        return True
    db.close()
    return False

def empty_db():
    f = "GodDog.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM users;')
    results = c.fetchall()
    return results == []
    
def check_pass(u):
    f = "GodDog.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    # print(username)
    c.execute('SELECT password FROM users WHERE username="%s";' %(u))
    results = c.fetchall()
    if results == []:
        db.close()
        return None
    else:
        db.close()
    return results[0][0]

def change_pw(u, p):
    f = "GodDog.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('UPDATE users SET password="%s" WHERE username="%s";' %(p, u))
    db.commit()
    db.close()
    return 
    
# pictures Database

# Sender - Receiver - Picture64 - Time
def add_picture(s, r, p, t):
    f = "GodDog.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    #c = init_cursor()
    c.execute('INSERT INTO pictures VALUES("%s", "%s", "%s", "%s");' %(s, r, p, t))
    db.commit()
    db.close()
    return True

def get_picture(s, r):
    c = init_cursor()
    c.execute('SELECT * FROM pictures WHERE sender="%s" AND receiver="%s";' %(s, r))
    results = c.fetchall()
    if results == []:
        db.close()
        return None
    else:
        db.close()
        return results

# messages Database

# Sender - Receiver - Message - Time
def add_message(s, r, m, t):
    c = init_cursor()
    c.execute('INSERT INTO messages VALUES("%s", "%s", "%s", "%s");' %(s, r, m, t))
    db.commit()
    db.close()
    return True

def get_message(s, r):
    c = init_cursor()
    c.execute('SELECT * FROM messages WHERE sender="%s" AND receiver="%s";' %(s, r))
    results = c.fetchall()
    if results == []:
        db.close()
        return None
    else:
        db.close()
        return results

# globalchat Database

# Sender - Message - Time
def add_global_message(s, m, t):
    c = init_cursor()
    c.execute('INSERT INTO globalchat VALUES("%s", "%s", "%s");' %(s, m, t))
    db.commit()
    db.close()
    return True

def get_global_message():
    c = init_cursor()
    c.execute('SELECT * FROM globalchat')
    results = c.fetchall()
    if results == []:
        db.close()
        return None
    else:
        db.close()
        return results
