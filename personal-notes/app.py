from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# notes = []

@app.route('/')
def index():
    if 'notes' not in session:
        session['notes'] = []  # Initialize empty notes list if it doesn't exist yet
    return render_template('index.html', notes=session['notes'])


@app.route('/add', methods=['POST'])
def add_note():
    note = request.form.get('note')
    if note:
        notes = session.get('notes', [])
        notes.append(note)
        session['notes'] = notes
        flash("Note added!", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:note_index>', methods=['POST'])
def delete_note(note_index):
    notes = session.get('notes', [])
    if 0 <= note_index < len(notes):
        notes.pop(note_index)
        session['notes'] = notes
        flash("Note deleted!", "danger")

    return redirect(url_for('index'))


    

if __name__=='__main__':
    app.run(debug=True)
