import sqlite3, os

basedir = os.path.abspath(os.path.dirname(__file__))
global db_file
db_file = basedir + "/../GodDog.db"

print db_file

db = sqlite3.connect(db_file)
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
    db = sqlite3.connect(db_file)
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
    db = sqlite3.connect(db_file)
    c = db.cursor()
    c.execute('SELECT * FROM users;')
    results = c.fetchall()
    return results == []
    
def check_pass(u):
    db = sqlite3.connect(db_file)
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
    db = sqlite3.connect(db_file)
    c = db.cursor()
    c.execute('UPDATE users SET password="%s" WHERE username="%s";' %(p, u))
    db.commit()
    db.close()
    return 
    
# pictures Database

# Sender - Receiver - Picture64 - Time
def add_picture(s, r, p, t):
    db = sqlite3.connect(db_file)
    c = db.cursor()
    #c = init_cursor()
    c.execute('INSERT INTO pictures VALUES("%s", "%s", "%s", "%s");' %(s, r, p, t))
    db.commit()
    db.close()
    return True

def get_picture(s, r):
    db = sqlite3.connect(db_file)
    c = db.cursor()
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
    db = sqlite3.connect(db_file)
    c = db.cursor()
    c.execute('INSERT INTO messages VALUES("%s", "%s", "%s", "%s");' %(s, r, m, t))
    db.commit()
    db.close()
    return True

def get_message(s, r):
    db = sqlite3.connect(db_file)
    c = db.cursor()
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
    db = sqlite3.connect(db_file)
    c = db.cursor()
    c.execute('INSERT INTO globalchat VALUES("%s", "%s", "%s");' %(s, m, t))
    db.commit()
    db.close()
    return True

def get_global_message():
    db = sqlite3.connect(db_file)
    c = db.cursor()
    c.execute('SELECT * FROM globalchat')
    results = c.fetchall()
    if results == []:
        db.close()
        return None
    else:
        db.close()
        return results


# friendslist database

# id - user1 - user2 - status
# id is id of friendship. every friendship has a unique id
# user1 is user who first initiated friendship
# user2 is user who is friended
# status: 
#     0: no love 
#     1: user1 loves user2 
#     2: user2 loves user1 
#     3: user1 loves user2 loves user1

# Gets the friends of a person
def f_getlist(user):
    db = sqlite3.connect(db_file)
    c = db.cursor()
    c.execute('SELECT * FROM friendslist WHERE user1="%s" OR user2="%s";'%(user, user))
    results = c.fetchall()  
    return results

# Checks if entry exists for that friendship already
# Returns: 
#     0: No entry exists 
#     1: user1 - user2 
#     2: user2 - user1
def f_listcheck(u1, u2):
    db = sqlite3.connect(db_file)
    c = db.cursor()
    c.execute('SELECT * FROM friendslist WHERE user1="%s" AND user2="%s";'%(u1, u2))
    results = c.fetchall()
    if results == []: # If user1 - user2 entry doesn't exist
        c.execute('SELECT * FROM friendslist WHERE user1="%s" AND user2="%s";' %(u2, u1))
        results = c.fetchall()
        if results == []: # If user2 - user1 entry doesn't exist
            db.close()
            return 0
        else: # Else user2 - user1 entry exists
            db.close()
            return 2
    else: # Else user1 - user2 entry exists
        db.close()
        return 1

# Returns the current status for displaying various buttons
# Returns:
#    0: Not friends (Display add friend)
#    1: Added friend (Display friends)
#    2: Mutual friends (Display mutual friend) 
def f_getstatus(u1, u2):
    db = sqlite3.connect(db_file)
    c = db.cursor()
    list_status = f_listcheck(u1, u2)
    if list_status == 0: # If the entry doesn't exist
        return 0
    else:
        cur_status = c.execute('SELECT status FROM friendslist WHERE user1="%s" and user2="%s";'%(u1, u2))
        if list_status == 1: # If user1 is in the user1 column
            if cur_status == 1: # If user1 has added user2 then display friends
                return 1
            elif cur_status == 3: # If both users are friends then display mutual friends
                return 2
            else: # Otherwise display add friend
                return 0
        elif list_status == 2: # If user1 is in the user2 column
            if cur_status == 2: # If user1 has added user2 then display friends
                return 1
            elif cur_status == 3: # If both users are friends then display mutual friends
                return 2
            else: # Otherwise display add friend
                return 0
        else: # All other scenarios display add friend
            return 0



# Updates the database
def f_dbupdate(action, list_status, u1, u2):
    db = sqlite3.connect(db_file)
    c = db.cursor()
    if action == 0: # If the action is to add friend
        if list_status == 0: # If the entry doesn't exist then add to database
            c.execute('INSERT INTO friendslist(user1, user2, status) VALUES("%s", "%s", 1);'%(u1, u2))
            db.commit()
            db.close()
            return True
        else: # Otherwise the entry exists
            cur_status = c.execute('SELECT status FROM friendslist WHERE user1="%s" AND user2="%s";'%(u1, u2))
            if list_status == 1: # If the user adding is in the user1 column
                if cur_status == 2: # If the other person has already added this user as a friend
                    c.execute('UPDATE friendslist SET status=3 WHERE user1="%s" AND user2="%s";'%(u1, u2))
                    db.commit()
                    db.close()
                    return True
                elif cur_status == 0: # If the entry already exists but the users have unfriended each other
                    c.execute('UPDATE friendslist SET status=1 WHERE user1="%s" AND user2="%s";'%(u1, u2))
                    db.commit()
                    db.close()
                    return True
                else: # Otherwise the user has already added this friend
                    return False
            elif list_status == 2: # If the user adding is in the user2 column
                if cur_status == 1: # If the other person has already added this user as a friend
                    c.execute('UPDATE friendslist SET status=3 WHERE user1="%s" AND user2="%s";'%(u1, u2))
                    db.commit()
                    db.close()
                    return True
                elif cur_status == 0: # If the entry already exists but the users have unfriended each other
                    c.execute('UPDATE friendslist SET status=2 WHERE user1="%s" AND user2="%s";'%(u1, u2))
                    db.commit()
                    db.close()
                    return True
                else: # Otherwise the user has already added this friend
                    return False
    else: # Otherwise action is remove friend
        cur_status = c.execute('SELECT status FROM friendslist WHERE user1="%s" AND user2="%s";'%(u1, u2))
        if list_status == 1: # If the user removing is in user1
            if cur_status == 1: # If user has added the friend but was not added back
                c.execute('UPDATE friendslist SET status=0 WHERE user1="%s" AND user2="%s";'%(u1, u2))
                db.commit()
                db.close()
                return True
            elif cur_status == 3: # If the users are mutual friends
                c.execute('UPDATE friendslist SET status=2 WHERE user1="%s" AND user2="%s"'%(u1, u2))
                db.commit()
                db.close()
                return True
            else: # Otherwise the user has already unfriended the friend
                return False
        elif list_status == 2: # If the user removing is in user2
            if cur_status == 2: # If the user has added the friend but was not added back
                c.execute('UPDATE friendslist SET status=0 WHERE user1="%s" AND user2="%s";'%(u1, u2))
                db.commit()
                db.close()
                return True
            elif cur_status == 3: # If the users are mutual friends
                c.execute('UPDATE friendslist SET status=1 WHERE user1="%s" AND user2="%s";'%(u1, u2))
                db.commit()
                db.close()
                return True
            else: # Otherwise the user has already unfriended the friend
                return False
        else: # Otherwise the users are not friends
            return False


# Adds the friendship / updates the friendship status
# u-user, f-friend to add
def add_friendship(u, f):
    list_status = f_listcheck(u, f)
    if list_status == 0 or list_status == 1: # If neither party has initiated a friendship or the user adding is in the user1 column
        result = f_dbupdate(0, list_status, u, f)
    elif list_status == 2: # If the user adding is in the user2 column
        result = f_dbupdate(0, list_status, f, u)
    else: # Otherwise the user has already added the friend as a friend
        return "Error: Already friends"
    return result

# Removes the friendship / updates the friendship status
# u-user, f-friend to remove
def remove_friendship(u, f):
    list_status = f_listcheck(u, f)
    if list_status == 1: # If the user removing is in the user1 column
        result = f_dbupdate(1, list_status, u, f)
    elif list_status == 2: # If the user removing is in the user2 column
        result = f_dbupdate(1, list_status, f, u)
    else: # Otherwise the user has already unfriended that friend
        return "Error: Not friends anyway"
    return result


    

        

