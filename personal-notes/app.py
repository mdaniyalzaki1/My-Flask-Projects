from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Note {self.id}>"


# notes = []

@app.route('/')
def index():
    # if 'notes' not in session:
    #     session['notes'] = []  
    notes = Note.query.all()
    return render_template('index.html', notes=notes)


@app.route('/add', methods=['POST'])
def add_note():
    note_content = request.form.get('note')
    if note_content:
        new_note = Note(content=note_content)
        db.session.add(new_note)
        db.session.commit()
        flash("Note added!", "success")
    return redirect(url_for('index'))


@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted!", "danger")
    return redirect(url_for('index'))

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if request.method == 'POST':
        new_content = request.form.get('note')
        if new_content:
            note.content = new_content
            db.session.commit()
            flash("Note updated!", "success")
            return redirect(url_for('index'))

    return render_template('edit.html', note=note)



    

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
