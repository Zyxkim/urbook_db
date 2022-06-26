import os
import random
import time

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import *
from . import db, UPLOAD_FOLDER
import json
import uuid

from .test_data.messages import messages
from .test_data.posts import posts
from .test_data.rooms import rooms
from .test_data.users import users

tests = Blueprint('tests', __name__)


@tests.route('/test_users', methods=['GET'])
def test_users():
    start = time.time()
    for elem in users:
        user_nickname = User.query.filter_by(nickname=elem['nickname']).first()
        user_email = User.query.filter_by(email=elem['email']).first()
        if user_email or user_nickname:
            continue
        new_user = User(email=elem['email'], status=elem['status'], nickname=elem['nickname'],
                        password=elem['password'])
        db.session.add(new_user)
        db.session.commit()
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}


@tests.route('/test_posts', methods=['GET'])
def test_posts():
    start = time.time()
    for elem in posts:
        new_post = Post(name=elem['name'], description=elem['description'], fandom=elem['fandom'],
                        content=elem['content'], user_id=random.randint(1, 500))
        db.session.add(new_post)
        db.session.commit()
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}


@tests.route('/test_rooms', methods=['GET'])
def test_rooms():
    start = time.time()
    for elem in rooms:
        new_room = Room(name=elem['name'], description=elem['description'])
        db.session.add(new_room)
        role = 'user'
        if random.randint(0, 1) == 0:
            role = 'admin'
        d = {
            'user_id': current_user.id,
            'room_id': new_room.id,
            'role': role
        }
        db.session.execute(user_room.insert(), params=d, )
        db.session.commit()
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}


@tests.route('/test_messages', methods=['GET'])
def test_messages():
    start = time.time()
    for elem in messages:
        new_message = Message(content=elem['content'], user_id=random.randint(1, 500), room_id=random.randint(1, 500))
        db.session.add(new_message)
        db.session.commit()
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}
