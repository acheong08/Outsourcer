#Main Flask
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, make_response, session
from werkzeug.exceptions import abort
import os.path
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c40a650584b50cb7d928f44d58dcaffc'
def getpass(username):
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    result = str(cursor.execute('SELECT password FROM accounts WHERE username = ?',
                            (username,)).fetchone())
    conn.close()
    return result

def getitems():
    conn = sqlite3.connect('items.db')
    conn.row_factory = sqlite3.Row
    return conn

def getcats():
    conn = sqlite3.connect('categories.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'username' in session:
        conn = getcats()
        cats = conn.execute('SELECT * FROM categories').fetchall()
        conn.close
        return render_template('home.html', account=session['username'], categories=cats)
    else:
        return render_template('login.html')

@app.route('/shop')
def shop():
        if 'username' in session:
            conn = getitems()
            items = conn.execute('SELECT * FROM items').fetchmany(5)
            conn.close()
            return render_template('store.html', items=items, categories=cats)
        else:
            return redirect(url_for('index'))
@app.route('/shop/<int:cat_id>')
def shopcat(cat_id):
    

        
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        truepass = getpass(username)
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        hashpass = str("('"+m.hexdigest()+"',)")
        if truepass is None:
            flash('User does not exist')
            return redirect(url_for('index'))
        elif truepass == hashpass:
            session['username'] = username
            flash("Logged in")
            return redirect(url_for('index'))
        else:
            flash("Wrong password")
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        if password == confirm:
            m5 = hashlib.md5()
            m5.update(password.encode('UTF-8'))
            hashpass = m5.hexdigest()
            users = getpass(username)
            if users == 'None':
                conn = sqlite3.connect('accounts.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)',
                            (username, hashpass))
                conn.commit()
                conn.close()
                session['username'] = username
                message = 'Logged in as: ', username
                flash(message)
                return redirect(url_for('index'))
            else:
                flash('User already exists')
                return redirect(url_for('signup'))
        else:
            flash('Passwords do not match')
            return redirect(url_for('signup'))
    elif request.method == 'GET':
        return render_template('signup.html')


@app.route('/logout', methods=('POST',))
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/admin', methods=('GET', 'POST'))
def admin():
    if request.method == 'GET':
        if 'isadmin' in session:
            return render_template('admin.html')
        else:
            return render_template('adminlogin.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        hashpass = str("('"+m.hexdigest()+"',)")
        conn = sqlite3.connect('admin.db')
        cursor = conn.cursor()
        truepass = str(cursor.execute('SELECT password FROM accounts WHERE username = ?',
                                    (username,)).fetchone())
        conn.close()
        if truepass == 'None':
            flash("Not an Admin User")
            return redirect(url_for('admin'))
        elif truepass != hashpass:
            flash("Wrong password")
            return redirect(url_for('admin'))
        elif truepass == hashpass:
            session['isadmin'] = True
            return redirect(url_for('admin'))
        else:
            flash('Oof... Something went wrong. Please tell the developer to revise the code')
            return redirect(url_for('adminlogin'))

@app.route('/admin/logout', methods=('POST',))
def adminlogout():
    session.pop('isadmin', None)
    return redirect(url_for('admin'))

def getadmins(username):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    result = str(cursor.execute('SELECT password FROM accounts WHERE username = ?',
                            (username,)).fetchone())
    conn.close()
    return result

@app.route('/admin/action', methods=('POST',))
def adminAction():
    if 'isadmin' in session:
        actionType = request.form['actionType']
        if actionType == 'DELUSER':
            deluser = request.form['deluser']
            if deluser != 'Admin':
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM accounts WHERE username = ?', (deluser,))
                conn.commit()
                conn.close()
                flash('User deleted')
            else:
                flash("Admin user cannot be deleted")
        elif actionType == 'ADDADMIN':
            username = request.form['adminuser']
            password = request.form['adminpassword']
            m5 = hashlib.md5()
            m5.update(password.encode('UTF-8'))
            hashpass = m5.hexdigest()
            admins = getadmins(username)
            if admins == 'None':
                conn = sqlite3.connect('admin.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)',
                            (username, hashpass))
                conn.commit()
                conn.close()
                flash('Success')
            else:
                flash('User Exists')
        elif actionType == 'DELADMIN':
            username = request.form['adminuser']
            exists = getadmins(username)
            if exists != 'None' and username != 'Admin':
                conn = sqlite3.connect('admin.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM accounts WHERE username = ?',
                            (username,))
                conn.commit()
                conn.close()
                flash('Success')
            else:
                flash('Cannot delete user')
        else:
            flash("No action specified")
        return redirect(url_for('admin'))
    else:
        flash("Permission denied")
        return redirect(url_for('index'))
@app.route('/admin/users')
def listusers():
    if 'isadmin' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        users = cursor.execute('SELECT * FROM accounts').fetchall()
        conn.close()
        return render_template('users.html', users=users)

def get_db_connection():
    conn = sqlite3.connect('items.db')
    conn.row_factory = sqlite3.Row
    return conn
def get_admin_connection():
    conn = sqlite3.connect('admin.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/admin/admins')
def listadmins():
    if 'isadmin' in session:
        conn = get_admin_connection()
        cursor = conn.cursor()
        users = cursor.execute('SELECT * FROM accounts').fetchall()
        conn.close()
        return render_template('adminlist.html', users=users)
