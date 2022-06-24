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

    follows = db.session.query(follower_followee).filter_by(follower_id=current_user.id).all()
    d, followed_user = {}, []
    for elem in follows:
        followee = User.query.filter_by(id=elem.followee_id).all()
        for data in followee:
            d = {
                'id': data.id,
                'nickname': data.nickname
            }
        followed_user.append(d)

    followees = db.session.query(follower_followee).filter_by(followee_id=current_user.id).all()
    b, followee_user = {}, []
    for elem in followees:
        follower = User.query.filter_by(id=elem.follower_id).all()
        for data in follower:
            b = {
                'id': data.id,
                'nickname': data.nickname
            }
        followee_user.append(b)

    post_name = request.args.get('text')
    if post_name:
        posts = Post.query.filter_by(name=post_name, user_id=current_user.id).all()
        return render_template("home.html", user=current_user, posts=posts, followed=followed_user, followers=followee_user)
    else:
        return render_template("home.html", user=current_user, posts=current_user.posts, followed=followed_user, followers=followee_user)


@views.route('/delete_post', methods=['GET'])
def delete_post():
    post_id = request.args.get('id')
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return render_template("home.html", user=current_user)


@views.route('/follows', methods=['GET', 'POST'])
def follows():
    follows = db.session.query(follower_followee).filter_by(follower_id=current_user.id).all()
    d, followed_user = {}, []
    for elem in follows:
        followee = User.query.filter_by(id=elem.followee_id).all()
        for data in followee:
            d = {
                'id': data.id,
                'nickname': data.nickname
            }
        followed_user.append(d)

    followees = db.session.query(follower_followee).filter_by(followee_id=current_user.id).all()
    b, followee_user = {}, []
    for elem in followees:
        follower = User.query.filter_by(id=elem.follower_id).all()
        for data in follower:
            b = {
                'id': data.id,
                'nickname': data.nickname
            }
        followee_user.append(b)

    return render_template("follows.html", user=current_user, followed=followed_user, followers=followee_user)


@views.route('/follow/<nickname>', methods=['GET', 'POST'])
@login_required
def follow(nickname):
    user_follow = User.query.filter_by(nickname=nickname).first()
    current_user.follow(user_follow)
    db.session.commit()


@views.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if request.method == 'POST':
        room_id = request.args.get('id')
        if room_id:
            content = request.form.get('content')

            if len(content) < 1:
                flash('Content is too short!', category='error')
            else:
                new_message = Message(content=content, user_id=current_user.id, room_id=room_id)
                db.session.add(new_message)
                db.session.commit()
                flash('Message sent!', category='success')

    room_name = request.args.get('text')
    if room_name:
        a = Room.query.filter_by(name=room_name).all()
    else:
        all_rooms = db.session.query(user_room).filter_by(user_id=current_user.id).all()
        d, a = {}, []
        for elem in all_rooms:
            room = Room.get(elem.room_id, None)
            a.append(room)
    return render_template("rooms.html", user=current_user, rooms=a)


@views.route('/create_room', methods=['POST'])
def create_room():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if len(name) < 1:
            flash('Name is too short!', category='error')
        else:
            new_room = Room(name=name, description=description)
            db.session.add(new_room)
            d = {
                'user_id': current_user.id,
                'room_id': new_room.id,
                'role': 'admin'
            }
            db.session.execute(user_room.insert(), params=d, )
            db.session.commit()
            flash('Room created!', category='success')

    all_rooms = db.session.query(user_room).filter_by(user_id=current_user.id).all()
    d, a = {}, []
    for elem in all_rooms:
        room = Room.get(elem.room_id, None)
        a.append(room)
    return render_template("rooms.html", user=current_user, rooms=a)


@views.route('/get_room_messages', methods=['GET'])
def get_room_messages():
    room_id = request.args.get('id')
    in_room = db.session.query(user_room).filter_by(user_id=current_user.id, room_id=room_id).first()
    if not in_room:
        d = {
            'user_id': current_user.id,
            'room_id': room_id,
            'role': 'user'
        }
        db.session.execute(user_room.insert(), params=d, )
        db.session.commit()

    all_messages = Message.get(None, room_id)
    room_name = Room.get(room_id, None).name
    d, a = {}, []
    for message in all_messages:
        d = {
            'id': message.id,
            'content': message.content,
            'creation_date': message.creation_date,
            'user_id': message.user_id,
            'user_nickname': User.query.filter_by(id=message.user_id).first().nickname,
            'room_id': message.room_id
        }
        a.append(d)
    return {'data': a, 'current_user': current_user.id, 'room_name': room_name}


@views.route('/get_role', methods=['GET'])
def get_role():
    room_id = request.args.get('id')
    in_room = db.session.query(user_room).filter_by(user_id=current_user.id, room_id=room_id).first()
    return {'role': in_room.role}

@views.route('/delete_room', methods=['GET'])
def delete_room():
    room_id = request.args.get('id')
    room = Room.query.get(room_id)
    db.session.query(user_room).filter_by(user_id=current_user.id, room_id=room_id).delete()
    Message.query.filter_by(room_id=room_id, user_id=current_user.id).delete()
    db.session.delete(room)
    db.session.commit()
    return {'SATUS': 'OK'}


@views.route('/leave_room', methods=['GET'])
def leave_room():
    room_id = request.args.get('id')
    db.session.query(user_room).filter_by(user_id=current_user.id, room_id=room_id).delete()
    db.session.commit()
    return {'SATUS': 'OK'}
