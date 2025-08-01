from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from functools import wraps
import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'a-fallback-secret-key-for-development')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --------------------- MODELS ------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    notes = db.relationship('Note', backref='owner', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Note {self.id}>"

# ------------------ DECORATORS & PROCESSORS --------------------

# Decorator to ensure a user is logged in before accessing a route
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor to make the current user and year available to all templates
@app.context_processor
def inject_user_and_year():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return dict(current_user=user, current_year=datetime.datetime.now().year)

# --------------------- ROUTES ------------------------

@app.route('/')
@login_required
def index():
    user_id = session['user_id'] # No need for .get() due to @login_required
    notes = Note.query.filter_by(user_id=user_id).order_by(Note.id.desc()).all()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
@login_required
def add_note():
    user_id = session['user_id']
    note_content = request.form.get('note')
    if note_content and note_content.strip(): # Ensure note is not just whitespace
        new_note = Note(content=note_content, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()
        flash("Note added!", "success")
    else:
        flash("Note content cannot be empty.", "danger")
    return redirect(url_for('index'))

@app.route('/delete/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != session['user_id']:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('index'))

    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "success") # Changed from danger to success/info
    return redirect(url_for('index'))

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != session['user_id']:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_content = request.form.get('note')
        if new_content and new_content.strip():
            note.content = new_content
            db.session.commit()
            flash("Note updated!", "success")
            return redirect(url_for('index'))
        else:
            flash("Note content cannot be empty.", "danger")

    return render_template('edit.html', note=note)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for('signup'))
        
        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
            return redirect(url_for('signup'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose another.", "danger")
            return redirect(url_for('signup'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        flash(f"Account created successfully! Welcome, {user.username}.", "success")
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash(f"Logged in successfully! Welcome back, {user.username}.", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# --------------------- CLI COMMANDS ------------------------

# Command to initialize the database: `flask init-db`
@app.cli.command("init-db")
def init_db_command():
    """Clears existing data and creates new tables."""
    db.create_all()
    print("Initialized the database.")

# --------------------- APP START ------------------------

if __name__ == '__main__':
    app.run(debug=True)