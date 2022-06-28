import random
import time

from flask import Blueprint
from .models import *
from . import db

from .test_data.images import images_profiles, images
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


@tests.route('/test_users_sql', methods=['GET'])
def test_users_sql():
    start = time.time()
    for elem in users:
        user_nickname = User.query.filter_by(nickname=elem['nickname']).first()
        user_email = User.query.filter_by(email=elem['email']).first()
        if user_email or user_nickname:
            continue
        db.engine.execute(
            "INSERT INTO \"user\"(email, nickname,status, password) VALUES(\'{}\', \'{}\', \'{}\', \'{}\')".format(
                elem['email'], elem['nickname'], elem['status'], elem['password']))
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


@tests.route('/test_posts_sql', methods=['GET'])
def test_posts_sql():
    start = time.time()
    for elem in posts:
        db.engine.execute(
            "INSERT INTO \"post\"(name, description,fandom, content,user_id) VALUES(\'{}\', \'{}\', \'{}\', \'{}\', {})".format(
                elem['name'], elem['description'], elem['fandom'], elem['content'], random.randint(1, 500)))
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}


@tests.route('/test_rooms', methods=['GET'])
def test_rooms():
    start = time.time()
    for elem in rooms:
        new_room = Room(name=elem['name'], description=elem['description'])
        db.session.add(new_room)
        db.session.commit()
        role = 'user'
        if random.randint(0, 1) == 0:
            role = 'admin'
        id = random.randint(1, 500)
        d = {
            'user_id': id,
            'room_id': new_room.id,
            'role': role
        }
        db.session.execute(user_room.insert(), params=d, )
        db.session.commit()
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}


@tests.route('/test_rooms_sql', methods=['GET'])
def test_rooms_sql():
    start = time.time()
    for elem in rooms:
        new_room = Room(name=elem['name'], description=elem['description'])
        db.session.add(new_room)
        db.session.commit()
        role = 'user'
        if random.randint(0, 1) == 0:
            role = 'admin'
        id = random.randint(1, 500)
        d = {
            'user_id': id,
            'room_id': new_room.id,
            'role': role
        }
        db.engine.execute(
            "INSERT INTO \"user_room\"(room_id, user_id,role) VALUES({}, {}, \'{}\')".format(new_room.id, id, role))
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

@tests.route('/test_messages_sql', methods=['GET'])
def test_messages_sql():
    start = time.time()
    for elem in messages:
        db.engine.execute(
            "INSERT INTO \"message\"(content, user_id,room_id) VALUES(\'{}\', {}, {})".format(elem['content'], random.randint(1, 500), random.randint(1, 500)))
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}

@tests.route('/test_follows', methods=['GET'])
def test_follows():
    start = time.time()
    for i in range(0, 250):
        id_1 = random.randint(1, 250)
        id_2 = random.randint(250, 500)
        if id_1 != id_2:
            user_follow = User.query.filter_by(id=id_1).first()
            user_followee = User.query.filter_by(id=id_2).first()
            user_followee.follow(user_follow)
            db.session.commit()
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}


@tests.route('/test_follows_sql', methods=['GET'])
def test_follows_sql():
    start = time.time()
    for i in range(0, 250):
        id_1 = random.randint(1, 250)
        id_2 = random.randint(250, 500)
        if id_1 != id_2:
            db.engine.execute(
                "INSERT INTO \"follower_followee\"(follower_id, followee_id) VALUES({}, {})".format(id_1, id_2))
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}


@tests.route('/test_images', methods=['GET'])
def test_images():
    start = time.time()
    for i in range(1, 500):
        new_image = Image(path=images_profiles[random.randint(0, len(images_profiles) - 1)], user_id=i)
        db.session.add(new_image)
        new_image = Image(path=images[random.randint(0, len(images) - 1)], post_id=i)
        db.session.add(new_image)
        new_image = Image(path=images[random.randint(0, len(images) - 1)], room_id=i)
        db.session.add(new_image)
    for i in range(0, 500, 20):
        new_image = Image(path=images[random.randint(0, len(images) - 1)], message_id=random.randint(1, 500))
        db.session.add(new_image)
    db.session.commit()
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}


@tests.route('/test_images_sql', methods=['GET'])
def test_images_sql():
    start = time.time()
    for i in range(1, 500):
        db.engine.execute(
            "INSERT INTO \"image\"(path, user_id) VALUES(\'{}\', {})".format(images_profiles[random.randint(0, len(images_profiles) - 1)], i))
        db.engine.execute(
            "INSERT INTO \"image\"(path, post_id) VALUES(\'{}\', {})".format(images[random.randint(0, len(images_profiles) - 1)], i))
        db.engine.execute(
            "INSERT INTO \"image\"(path, room_id) VALUES(\'{}\', {})".format(images[random.randint(0, len(images_profiles) - 1)], i))
    for i in range(0, 500, 20):
        db.engine.execute(
            "INSERT INTO \"image\"(path, message_id) VALUES(\'{}\', {})".format(images[random.randint(0, len(images_profiles) - 1)], random.randint(1, 500)))
    end = time.time()
    return {'Status': 'OK', 'time': (end - start)}
