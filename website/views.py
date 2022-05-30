from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        name = request.form.get('name')
        fandom = request.form.get('fandom')
        description = request.form.get('description')
        content = request.form.get('content')

        if len(name) < 1:
            flash('Name is too short!', category='error')
        else:
            new_post = Post(name=name, description=description, fandom=fandom, content=content, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post added!', category='success')
    return render_template("create_post.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
