from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

user_room = db.Table('user_room',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('room_id', db.Integer, db.ForeignKey('room.id'), primary_key=True),
                     db.Column('role', db.String(5))
                     )

follower_followee = db.Table('follower_followee',
                             db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                             db.Column('followee_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                             )


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(88), nullable=False)
    nickname = db.Column(db.String(150), unique=True, nullable=False)
    status = db.Column(db.String(255), nullable=True)
    registration_date = db.Column(db.DateTime(timezone=True), default=func.now())

    posts = db.relationship('Post')
    messages = db.relationship('Message', backref='user', lazy=True)
    user_room = db.relationship('Room', secondary=user_room, lazy='subquery', backref=db.backref('rooms', lazy=True))
    follower_followee = db.relationship(
        'User', secondary=follower_followee,
        primaryjoin=(follower_followee.c.follower_id == id),
        secondaryjoin=(follower_followee.c.followee_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    image = db.relationship('Image', backref='user', lazy=True)

    def follow(self, user):
        if not self.is_following(user):
            self.follower_followee.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.follower_followee.remove(user)

    def is_following(self, user):
        return self.follower_followee.filter(
            follower_followee.c.follower_id == user.id).count() > 0


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    messages = db.relationship('Message', backref='room', lazy=True)
    image = db.relationship('Image', backref='room', lazy=True)


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    fandom = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.relationship('Image', backref='post', lazy=True)


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
