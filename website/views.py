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
    return render_template("home.html", user=current_user)

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

@views.route('/follows', methods=['GET', 'POST'])
def follows():
    return render_template("follows.html", user=current_user)

@views.route('/follow/<nickname>', methods=['GET', 'POST'])
@login_required
def follow(nickname):
    user_follow = User.query.filter_by(nickname=nickname).first()
    current_user.follow(user_follow)
    db.session.commit()

@views.route('/rooms', methods=['GET', 'POST'])
def rooms():
    all_rooms = db.engine.execute("SELECT * FROM room order by creation_date")
    return render_template("rooms.html", user=current_user, rooms=all_rooms)

@views.route('/get_all_rooms', methods=['GET'])
def get_all_rooms():
    all_rooms = db.engine.execute("SELECT * FROM room order by creation_date")
    d, a = {}, []
    for rowproxy in all_rooms:
        for column, value in rowproxy.items():
            d = {**d, **{column: value}}
        a.append(d)
    return {'data' : a}