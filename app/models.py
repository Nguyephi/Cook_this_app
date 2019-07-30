from flask_sqlalchemy import SQLAlchemy, current_app
from flask_login import UserMixin, LoginManager
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class Subscribe(db.Model):
    __tablename__ = 'subscribe'
    # id = db.Column(db.Integer, primary_key=True)
    subscriber = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    user_subscribed = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True)
    is_subscribed = db.Column(db.Boolean, default=False)


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(255), unique=True)
    dob = db.Column(db.String(50))
    # Make sure to change this to be available in the SelectField
    gender = db.Column(db.String(15))
    bio = db.Column(db.String(500))
    provider = db.Column(db.String(100))
    provider_id = db.Column(db.Integer)
    provider_pic = db.Column(db.String)
    date_created = db.Column(db.DateTime)
    password = db.Column(db.String(255))

    comments = db.relationship('Comments', backref='user')

    subscriber = db.relationship(
        'Subscribe', backref='follower', primaryjoin=(id == Subscribe.subscriber))
    user_subscribed = db.relationship(
        'Subscribe', backref='following', primaryjoin=(id == Subscribe.user_subscribed))

    def __repr__(self):
        return '<User {}self.username'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Recipes(db.Model):
    __tablename__: 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    user = db.relationship(Users)
    title = db.Column(db.String(255))
    description = db.Column(db.String(2200))
    date_created = db.Column(db.DateTime)
    comments = db.relationship('Comments', backref='post')
    imgUrl = db.Column(db.String)


class isLikes(db.Model):
    __tablename__: 'is_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    post_id = db.Column(db.Integer, db.ForeignKey(Recipes.id))
    user = db.relationship(Users)
    post = db.relationship(Recipes)
    is_liked = db.Column(db.Boolean, default=False)


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    post_id = db.Column(db.Integer, db.ForeignKey(Recipes.id))
    comment = db.Column(db.String(2200))
    date_posted = db.Column(db.DateTime)


class Ingredients(db.Model):
    __tablename__: 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipes.id))
    recipe = db.relationship(Recipes, backref='ingredients')
    ingredient = db.Column(db.String(255))
    ingredient_id = db.Column(db.Integer)
    quantity = db.Column(db.String)


class Instructions(db.Model):
    __tablename__: 'instructions'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipes.id))
    recipe = db.relationship(Recipes, backref='instructions')
    instruction = db.Column(db.String)
    instruction_id = db.Column(db.Integer)


class OAuth(OAuthConsumerMixin, db.Model):
    __tablename__ = 'OAuth'
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    user = db.relationship(Users)


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    user = db.relationship(Users)


# setup login manager
login_manager = LoginManager()
# login_manager.login_view = "facebook.login"


@login_manager.user_loader
def load_user(user_id):
    # print(__name__, 'user_loader', user_id)
    return Users.query.get(int(user_id))


@login_manager.request_loader
def load_user_from_request(request):
    # Login Using our Custom Header
    api_key = request.headers.get('Authorization')
    # print(__func__, 'xxxx')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            # print(__func__, 'request_loader')
            return token.user

    return None
