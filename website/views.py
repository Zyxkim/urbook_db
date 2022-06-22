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
    follows = db.engine.execute("SELECT * FROM follower_followee where follower_id=%s", (current_user.id))
    d, followed_user = {}, []
    for elem in follows:
        followee = User.query.filter_by(id=elem.followee_id).all()
        print(followee)
        for data in followee:
            d = {
                'id': data.id,
                'nickname': data.nickname
            }
        followed_user.append(d)
    print(followed_user)

    followees = db.engine.execute("SELECT * FROM follower_followee where followee_id=%s", (current_user.id))
    b, followee_user = {}, []
    for elem in followees:
        follower = User.query.filter_by(id=elem.follower_id).all()
        print(follower)
        for data in follower:
            b = {
                'id': data.id,
                'nickname': data.nickname
            }
        followee_user.append(b)
    print(followee_user)

    return render_template("follows.html", user=current_user, followed=followed_user, followers=followee_user)


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


@views.route('/rooms/<room>/<nickname>', methods=['GET', 'POST'])
@login_required
def join(room, nickname):
    user_room = User.query.filter_by(nickname=nickname).first()
    current_user.join_room(user_room)
    db.session.commit()


@views.route('/get_user_rooms', methods=['GET'])
def get_all_rooms():
    all_rooms = db.engine.execute("SELECT * FROM user_room where user_id=%s", (current_user.id))
    d, a = {}, []
    for elem in all_rooms:
        room = db.engine.execute("SELECT * FROM room where id=%s", (elem.room_id))
        for rowproxy in room:
            print(rowproxy)
        for column, value in rowproxy.items():
            d = {**d, **{column: value}, 'role': elem.role}
        a.append(d)
    print(a)
    return {'data': a}
