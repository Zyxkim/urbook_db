import os

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import *
from . import db, UPLOAD_FOLDER
import json
import uuid

views = Blueprint('views', __name__)
DATA_SERVER = 'http://localhost:8000/'


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
    if request.method == 'POST':
        name = request.form.get('name')
        fandom = request.form.get('fandom')
        description = request.form.get('description')
        content = request.form.get('content')
        file = request.files['file']

        if len(name) < 1:
            flash('Name is too short!', category='error')
        else:
            new_post = Post(name=name, description=description, fandom=fandom, content=content, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()

            if file:
                filename = str(uuid.uuid4()) + '.jpg'
                path = os.path.join(UPLOAD_FOLDER, filename)
                new_image = Image(path=DATA_SERVER + filename, post_id=new_post.id)
                db.session.add(new_image)
                file.save(path)
                db.session.commit()

            flash('Post added!', category='success')

    follows = db.session.query(follower_followee).filter_by(follower_id=current_user.id).all()
    d, followed_user = {}, []
    for elem in follows:
        followee = User.query.filter_by(id=elem.followee_id).all()
        for data in followee:
            image = Image.query.filter_by(user_id=data.id).first()
            if image:
                image_path = image.path
            else:
                image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            d = {
                'id': data.id,
                'nickname': data.nickname,
                'image_path': image_path
            }
        followed_user.append(d)

    followees = db.session.query(follower_followee).filter_by(followee_id=current_user.id).all()
    b, followee_user = {}, []
    for elem in followees:
        follower = User.query.filter_by(id=elem.follower_id).all()
        for data in follower:
            image = Image.query.filter_by(user_id=data.id).first()
            if image:
                image_path = image.path
            else:
                image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            b = {
                'id': data.id,
                'nickname': data.nickname,
                'image_path': image_path
            }
        followee_user.append(b)

    post_name = request.args.get('text')

    image = Image.query.filter_by(user_id=current_user.id).first()
    image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
    if image:
        image_path = image.path
    if post_name:
        posts = Post.query.filter_by(name=post_name, user_id=current_user.id).all()

        posts_with_photos = []
        for data in posts:
            image = Image.query.filter_by(post_id=data.id).first()
            if image:
                image_path_post = image.path
            else:
                image_path_post = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            data.image_path = image_path_post
            posts_with_photos.append(data)
        return render_template("home.html", user=current_user, posts=posts_with_photos, followed=followed_user,
                               followers=followee_user, image_path=image_path)
    else:
        posts_with_photos = []
        for data in current_user.posts:
            image = Image.query.filter_by(post_id=data.id).first()
            if image:
                image_path_post = image.path
            else:
                image_path_post = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            data.image_path = image_path_post
            posts_with_photos.append(data)
        return render_template("home.html", user=current_user, posts=posts_with_photos, followed=followed_user,
                               followers=followee_user, image_path=image_path)


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
            image = Image.query.filter_by(user_id=data.id).first()
            if image:
                image_path = image.path
            else:
                image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            d = {
                'id': data.id,
                'nickname': data.nickname,
                'image_path': image_path
            }
        followed_user.append(d)

    followees = db.session.query(follower_followee).filter_by(followee_id=current_user.id).all()
    b, followee_user = {}, []
    for elem in followees:
        follower = User.query.filter_by(id=elem.follower_id).all()
        for data in follower:
            image = Image.query.filter_by(user_id=data.id).first()
            if image:
                image_path = image.path
            else:
                image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            b = {
                'id': data.id,
                'nickname': data.nickname,
                'image_path': image_path
            }
        followee_user.append(b)

    return render_template("follows.html", user=current_user, followed=followed_user, followers=followee_user)


@views.route('/rooms', methods=['GET', 'POST'])
def rooms():
    room_id = request.args.get('id')
    image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
    if request.method == 'POST':
        file = request.files['file']
        if room_id:
            content = request.form.get('content')

            if len(content) < 1:
                flash('Content is too short!', category='error')
            else:
                new_message = Message(content=content, user_id=current_user.id, room_id=room_id)
                db.session.add(new_message)
                db.session.commit()

                if file:
                    filename = str(uuid.uuid4()) + '.jpg'
                    path = os.path.join(UPLOAD_FOLDER, filename)
                    image = Image.query.filter_by(message_id=new_message.id).first()
                    if image:
                        os.remove(UPLOAD_FOLDER + '\\' + image.path.split('/')[-1])
                        image.path = DATA_SERVER + filename
                    else:
                        new_image = Image(path=DATA_SERVER + filename, message_id=new_message.id)
                        db.session.add(new_image)
                    file.save(path)
                    db.session.commit()
                flash('Message sent!', category='success')

    room_name = request.args.get('text')
    if room_name:
        all_rooms = Room.query.filter_by(name=room_name).all()
        d, a = {}, []
        for elem in all_rooms:
            room = Room.get(elem.id, None)
            b = room

            image = Image.query.filter_by(room_id=elem.id).first()
            if image:
                image_path = image.path
            else:
                image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            b.image_path = image_path
            a.append(b)
    else:
        all_rooms = db.session.query(user_room).filter_by(user_id=current_user.id).all()
        d, a = {}, []
        for elem in all_rooms:
            room = Room.get(elem.room_id, None)
            b = room

            image = Image.query.filter_by(room_id=room.id).first()
            if image:
                image_path = image.path
            else:
                image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            b.image_path = image_path
            a.append(b)
    room = Room.query.filter_by(id=room_id).first()
    if room:
        room_name = room.name
        room_description = room.description
        image = Image.query.filter_by(room_id=room.id).first()
        if image:
            image_path = image.path
        else:
            image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
    else:
        room_name = None
        room_description = None
        image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
    return render_template("rooms.html", user=current_user, rooms=a, room_id=room_id, room_name=room_name,
                           room_description=room_description, image_path=image_path)


@views.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        file = request.files['file']

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

            if file:
                filename = str(uuid.uuid4()) + '.jpg'
                path = os.path.join(UPLOAD_FOLDER, filename)
                new_image = Image(path=DATA_SERVER + filename, room_id=new_room.id)
                db.session.add(new_image)
                file.save(path)
                db.session.commit()

            flash('Room created!', category='success')

    all_rooms = db.session.query(user_room).filter_by(user_id=current_user.id).all()
    d, a = {}, []
    for elem in all_rooms:
        room = Room.get(elem.room_id, None)
        a.append(room)
    return redirect(url_for('views.rooms'))


@views.route('/edit_room', methods=['GET', 'POST'])
def edit_room():
    room_id = request.args.get('id')
    name = request.form.get('name')
    description = request.form.get('description')
    file = request.files['file']

    image = Image.query.filter_by(room_id=room_id).first()

    room = Room.query.filter_by(id=room_id).first()
    if name:
        room.name = name
    if description:
        room.description = description

    if file:
        filename = str(uuid.uuid4()) + '.jpg'
        path = os.path.join(UPLOAD_FOLDER, filename)

        if image:
            os.remove(UPLOAD_FOLDER + '\\' + image.path.split('/')[-1])
            image.path = DATA_SERVER + filename
        else:
            new_image = Image(path=DATA_SERVER + filename, room_id=room_id)
            db.session.add(new_image)
        file.save(path)

    db.session.commit()

    return redirect('/rooms?id=' + room_id)


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
        return redirect('/rooms?id=' + room_id)

    all_messages = Message.get(None, room_id)
    room_name = Room.get(room_id, None).name
    d, a = {}, []
    for message in all_messages:
        image = Image.query.filter_by(message_id=message.id).first()
        if image:
            image_path = image.path
        else:
            image_path = None
        d = {
            'id': message.id,
            'content': message.content,
            'creation_date': message.creation_date,
            'user_id': message.user_id,
            'user_nickname': User.query.filter_by(id=message.user_id).first().nickname,
            'room_id': message.room_id,
            'image_path': image_path
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


@views.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    user_id = request.args.get('id')

    if user_id == str(current_user.id):
        return redirect('/')

    user = User.query.filter_by(id=user_id).first()
    follows = db.session.query(follower_followee).filter_by(follower_id=user_id).all()
    d, followed_user = {}, []
    for elem in follows:
        followee = User.query.filter_by(id=elem.followee_id).all()
        for data in followee:
            image = Image.query.filter_by(user_id=data.id).first()
            if image:
                image_path = image.path
            else:
                image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            d = {
                'id': data.id,
                'nickname': data.nickname,
                'image_path': image_path
            }
        followed_user.append(d)

    followees = db.session.query(follower_followee).filter_by(followee_id=user_id).all()
    b, followee_user = {}, []
    for elem in followees:
        follower = User.query.filter_by(id=elem.follower_id).all()
        for data in follower:
            image = Image.query.filter_by(user_id=data.id).first()
            if image:
                image_path = image.path
            else:
                image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            b = {
                'id': data.id,
                'nickname': data.nickname,
                'image_path': image_path
            }
        followee_user.append(b)

    is_following = db.session.query(follower_followee).filter_by(follower_id=current_user.id,
                                                                 followee_id=user_id).first()
    if is_following:
        is_following = 1
    else:
        is_following = 0

    image = Image.query.filter_by(user_id=user_id).first()
    image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
    if image:
        image_path = image.path

    post_name = request.args.get('text')
    if post_name:
        posts = Post.query.filter_by(name=post_name, user_id=user_id).all()

        posts_with_photos = []
        for data in posts:
            image = Image.query.filter_by(post_id=data.id).first()
            if image:
                image_path_post = image.path
            else:
                image_path_post = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            data.image_path = image_path_post
            posts_with_photos.append(data)

        return render_template("user.html", user=user, posts=posts_with_photos, followed=followed_user,
                               followers=followee_user, is_following=is_following, image_path=image_path)
    else:
        posts = Post.query.filter_by(user_id=user_id).all()

        posts_with_photos = []
        for data in posts:
            image = Image.query.filter_by(post_id=data.id).first()
            if image:
                image_path_post = image.path
            else:
                image_path_post = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
            data.image_path = image_path_post
            posts_with_photos.append(data)

        return render_template("user.html", user=user, posts=posts_with_photos, followed=followed_user,
                               followers=followee_user, is_following=is_following, image_path=image_path)


@views.route('/follow', methods=['GET', 'POST'])
@login_required
def follow():
    user_id = request.args.get('id')
    user_follow = User.query.filter_by(id=user_id).first()
    current_user.follow(user_follow)
    db.session.commit()
    return {'Status': 'OK'}


@views.route('/unfollow', methods=['GET', 'POST'])
@login_required
def unfollow():
    user_id = request.args.get('id')
    user_follow = User.query.filter_by(id=user_id).first()
    current_user.unfollow(user_follow)
    db.session.commit()
    return {'Status': 'OK'}


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    image = Image.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        email = request.form.get('email')
        nickname = request.form.get('firstName')
        status = request.form.get('status')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        file = request.files['file']

        user = User.query.filter_by(email=email).first()
        user_nickname = User.query.filter_by(nickname=nickname).first()

        if user:
            flash('Аккаунт с таким e-mail существует.', category='error')
        elif email:
            if len(email) < 4:
                flash('Минимальная длина e-mail - 4 символа.', category='error')
            else:
                current_user.email = email
                db.session.commit()

        if user_nickname:
            flash('Аккаунт с таким nickname существует.', category='error')
        elif nickname:
            if len(nickname) < 2:
                flash('Минимальная длина ника - 2 символа.', category='error')
            else:
                current_user.nickname = nickname
                db.session.commit()

        if status:
            current_user.status = status
            db.session.commit()

        if password1:
            if len(password1) < 4:
                flash('Минимальная длина pass - 4 символа.', category='error')
            elif password1 != password2:
                flash('Пароли не совпадают.', category='error')
            else:
                current_user.password = generate_password_hash(password1, method='sha256')
                db.session.commit()

        if file:
            filename = str(uuid.uuid4()) + '.jpg'
            path = os.path.join(UPLOAD_FOLDER, filename)

            if image:
                os.remove(UPLOAD_FOLDER + '\\' + image.path.split('/')[-1])
                image.path = DATA_SERVER + filename
            else:
                new_image = Image(path=DATA_SERVER + filename, user_id=current_user.id)
                db.session.add(new_image)
            file.save(path)
            db.session.commit()
            return redirect('/settings')

    # return redirect(url_for('views.home'))
    image_path = 'https://catherineasquithgallery.com/uploads/posts/2021-02/1614507972_15-p-yarko-belii-fon-24.jpg'
    if image:
        image_path = image.path
    return render_template("settings.html", user=current_user, image_path=image_path)
