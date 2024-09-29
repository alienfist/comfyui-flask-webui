from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from datetime import datetime
import logging
from utils.common import get_md5
from ext import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), unique=True, nullable=False, index=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.Integer, default=1)
    status = db.Column(db.Integer, default=2)
    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), unique=True, nullable=False, index=True)
    image_url = db.Column(db.String(255), nullable=False)
    params = db.Column(db.Text)
    image_type = db.Column(db.Integer)
    status = db.Column(db.Integer, default=2)
    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # foreign key
    user_uuid = db.Column(db.String(32), db.ForeignKey('users.uuid', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('images', lazy=True))

    def __repr__(self):
        return f"Image(id={self.id}, uuid='{self.uuid}')"


def create_user(username, password, email, role):
    try:
        if User.query.filter_by(username=username).first():
            return None, "user exists."
        hashed_password = generate_password_hash(password)
        uuid = get_md5(f"username:{username}", 16)
        new_user = User(uuid=uuid, username=username, password=hashed_password, email=email, role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user, "Create user success."
    except Exception as e:
        logging.exception('An exception occurred: %s', e)
        return None, "Create user failed."


def get_user_by_username(username):
    try:
        return User.query.filter_by(username=username).first()
    except Exception as e:
        logging.exception('An exception occurred: %s', e)
        return None


def update_user_password(username, new_password):
    try:
        user = get_user_by_username(username)
        if not user:
            return None
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return user
    except Exception as e:
        logging.exception('An exception occurred: %s', e)
        return None


def delete_user(username):
    try:
        user = get_user_by_username(username)
        if not user:
            return None
        user.status = 7
        db.session.commit()
        return user
    except Exception as e:
        logging.exception('An exception occurred: %s', e)
        return None


def create_image(image_url, params, image_type, user_uuid):
    try:
        uuid = get_md5(f"image:{image_url}", 20)
        new_image = Image(uuid=uuid, image_url=image_url, params=params, image_type=image_type, user_uuid=user_uuid)
        db.session.add(new_image)
        db.session.commit()
        return new_image
    except Exception as e:
        logging.exception('An exception occurred: %s', e)
        return None


def get_image_by_id(image_id):
    try:
        return Image.query.get(image_id)
    except Exception as e:
        logging.exception('An exception occurred: %s', e)
        return None


def get_images_by_page_and_user(per_page, offset, user_uuid):
    try:
        return Image.query.filter_by(user_uuid=user_uuid, status=2).order_by(Image.create_time.desc()).limit(per_page).offset(offset).all()
    except Exception as e:
        logging.exception('An exception occurred: %s', e)
        return None


def update_image(image_id, image_url=None, params=None, image_type=None):
    try:
        image = get_image_by_id(image_id)
        if not image:
            return None
        if image_url:
            image.image_url = image_url
        if params:
            image.params = params
        if image_type:
            image.image_type = image_type
        db.session.commit()
        return image
    except Exception as e:
        logging.exception('An exception occurred: %s', e)
        return None


def delete_image(image_id):
    try:
        image = get_image_by_id(image_id)
        if not image:
            return None
        image.status = 7
        db.session.commit()
        return image
    except Exception as e:
        logging.exception('An exception occurred: %s', e)
        return None
