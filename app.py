from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, jsonify
import os
import json
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
USER_FILE = 'users.json'
FILES_FILE = 'files.json'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

def load_files():
    if os.path.exists(FILES_FILE):
        with open(FILES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_files(files):
    with open(FILES_FILE, 'w') as f:
        json.dump(files, f)

def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

@app.route('/')
def index():
    if 'email' in session:
        files = load_files().get(session['email'], [])
        return render_template('index.html', files=files)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not is_valid_email(email):
            return 'Ungültige E-Mail-Adresse!'
        users = load_users()
        if email in users:
            return 'Benutzer existiert bereits!'
        users[email] = password  # Speichern des Passworts im Klartext
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if email in users and users[email] == password:  # Überprüfung des Klartext-Passworts
            session['email'] = email
            return jsonify(success=True)
        return jsonify(success=False)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'email' not in session:
        return redirect(url_for('login'))
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        files = load_files()
        user_files = files.get(session['email'], [])
        user_files.append(file.filename)
        files[session['email']] = user_files
        save_files(files)
        return redirect(url_for('index'))

@app.route('/uploads/')
def uploaded_file(filename):
    if 'email' not in session:
        return redirect(url_for('login'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/', methods=['POST'])
def delete_file(filename):
    if 'email' not in session:
        return redirect(url_for('login'))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        files = load_files()
        user_files = files.get(session['email'], [])
        user_files.remove(filename)
        files[session['email']] = user_files
        save_files(files)
    return redirect(url_for('index'))

@app.route('/users')
def get_users():
    if 'email' not in session:
        return redirect(url_for('login'))
    users = load_users()
    return render_template('users.html', users=users)

@app.route('/files')
def get_files():
    if 'email' not in session:
        return redirect(url_for('login'))
    files = load_files()
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8690)