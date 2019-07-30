import os
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required, logout_user, login_user
from flask_migrate import Migrate
from .models import db, login_manager, Users, Token, Recipes, Ingredients, Instructions, isLikes, Subscribe, Comments
from .forms import SignUpForm, CreateRecipeForm
from .oauth import blueprint
from .config import Config
from .cli import create_db
from flask_cors import CORS
import wtforms_json
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
wtforms_json.init()


db.init_app(app)
migrate = Migrate(app, db, compare_type=True)
login_manager.init_app(app)
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(create_db)

# POSTGRES = {
#     'user': os.environ['POSTGRES_USER'],
#     'pw': os.environ['POSTGRES_PWD'],
#     'db': os.environ['POSTGRES_DB'],
#     'host': os.environ['POSTGRES_HOST'],
#     'port': os.environ['POSTGRES_PORT'],
# }

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:\
# %(port)s/%(db)s' % POSTGRES
# print(app.config['SQLALCHEMY_DATABASE_URI'])

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def index():
    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    token = Token.query.filter_by(user_id=current_user.id).first()
    db.session.delete(token)
    db.session.commit()
    logout_user()
    flash("You have logged out")
    return jsonify({'status': "ok"})


@app.route('/createaccount', methods=['POST', 'GET'])
def create_account():
    form = SignUpForm.from_json(request.json)
    if form.validate():
        new_user = Users(name=form.name.data,
                         username=form.username.data,
                         email=form.email.data,
                         date_created=datetime.now()
                         )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
    return jsonify({'errors': form.errors})


@app.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    user = Users.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        token = Token(user_id=user.id, uuid=uuid.uuid4().hex)
        db.session.add(token)
        db.session.commit()
        login_user(user)

        return jsonify({'success': 'true',
                        'token': token.uuid,
                        'username': user.username,
                        'name': user.name,
                        'email': user.email,

                        })
    else:
        return jsonify({'success': 'false',
                        'message': {
                            'email': 'Invalid email',
                            'password': 'Incorrect password'}})


@app.route('/userdata', methods=['GET'])
@login_required
def userdata():
    user = Users.query.filter_by(id=current_user.id).first()
    post = Recipes.query.filter_by(
        user_id=current_user.id).all()
    following = Subscribe.query.filter_by(
        subscriber=current_user.id, is_subscribed=True).all()
    follower = Subscribe.query.filter_by(
        user_subscribed=current_user.id, is_subscribed=True).all()
    total_post = len(post)
    total_following = len(following)
    total_follower = len(follower)
    sending = {'name': user.name,
               'email': user.email,
               'username': user.username,
               'avatar': user.provider_pic,
               'id': user.id,
               'total_post': total_post,
               'total_follower': total_follower,
               'total_following': total_following}
    return jsonify(sending)


@app.route('/usersubscription', methods=['GET'])
@login_required
def usersubscription():
    user = Users.query.filter_by(id=current_user.id).first()
    following = Subscribe.query.filter_by(
        subscriber=current_user.id, is_subscribed=True).all()
    follower = Subscribe.query.filter_by(
        user_subscribed=current_user.id, is_subscribed=True).all()
    subscribing = [{'subscribing_username': i.following.username,
                    'subscribing_name': i.following.name} for i in following]
    subscriber = [{'subscriber_username': j.follower.username,
                   'subscriber_name': j.follower.name}for j in follower]
    sending = {'user_subscription': {
        'subscribing': subscribing,
        'subscriber': subscriber
    }}
    return jsonify(sending)


@app.route('/getotheruserdata/<user_id>', methods=['GET', 'POST'])
@login_required
def getotheruserdata(user_id):
    user = Users.query.filter_by(id=user_id).first()
    post = Recipes.query.filter_by(
        user_id=user.id).all()
    following = Subscribe.query.filter_by(
        subscriber=user_id, is_subscribed=True).all()
    follower = Subscribe.query.filter_by(
        user_subscribed=user_id, is_subscribed=True).all()
    total_post = len(post)
    total_following = len(following)
    total_follower = len(follower)
    sending = {'name': user.name,
               'username': user.username,
               'avatar': user.provider_pic,
               'id': user.id,
               'total_post': total_post,
               'total_follower': total_follower,
               'total_following': total_following,
               "recipes": [{'title': k.title,
                            'imgUrl': k.imgUrl,
                            'id': k.id} for k in post]}
    return jsonify(sending)


@app.route('/createrecipe', methods=['POST', 'GET'])
@login_required
def create_recipe():
    data = request.get_json()
    if request.method == 'POST':
        title = Recipes(
            title=data['title'],
            description=data['description'],
            user_id=current_user.id,
            imgUrl=data['imgUrl'],
            date_created=datetime.now()
        )
        db.session.add(title)
        db.session.commit()
        for i in data['ingredients']:
            new_ingredient = Ingredients(recipe_id=title.id,
                                         ingredient_id=int(i['id']), ingredient=i['name'], quantity=i['quantity'])

            db.session.add(new_ingredient)
        for i in data['instructions']:
            new_instruction = Instructions(recipe_id=title.id,
                                           instruction_id=int(i['id']), instruction=i['name'])
            db.session.add(new_instruction)
            db.session.commit()
    return jsonify({"success": "ok"})


@app.route('/updateaccount', methods=['POST', 'GET'])
@login_required
def update_account():
    # user = Users.query.filter_by(id=current_user.id).first()
    info = request.get_json()
    update = Users.query.filter_by(id=current_user.id).first()
    sending = {"success": "false"}
    if info['username'] != '':
        update.username = info['username']
        sending = {'success': "true"}
    if info['email'] != '':
        update.email = info['email']
        sending = {'success': "true"}
    if info['name'] != '':
        update.name = info['name']
        sending = {'success': "true"}
    db.session.commit()
    return jsonify(sending)


@app.route('/recipedata', methods=['GET', 'POST'])
@login_required
def recipedata():
    recipes = Recipes.query.all()
    send_recipe_data = {"recipes": [{'post_id': i.id,
                                     'created_by': i.user.username,
                                     'creator_id': i.user.id,
                                     'creator_avatar': i.user.provider_pic,
                                     'title': i.title,
                                     'description': i.description,
                                     'imgUrl': i.imgUrl,
                                     'date_created': i.date_created,
                                     'ingredients': [{'ingredient': j.ingredient,
                                                      'quantity': j.quantity} for j in Ingredients.query.filter(Ingredients.recipe_id == i.id).all()],
                                     'instructions': [k.instruction for k in Instructions.query.filter(Instructions.recipe_id == i.id).all()],
                                     'comments': [{'comment': l.comment, 'user': l.user.username} for l in Comments.query.filter(Comments.post_id == i.id).all()],
                                     'liked': check_liked(recipe_id=i.id)
                                     } for i in recipes]}
    return jsonify(send_recipe_data)


def check_liked(user=current_user, recipe_id=None):
    is_like = isLikes.query.filter_by(
        post_id=recipe_id, user_id=user.id).first()
    if (is_like is None) or is_like.is_liked == 0:
        return False
    return True


@app.route('/singlerecipedata/<post_id>', methods=['POST', 'GET'])
@login_required
def singlerecipedata(post_id):
    recipe = Recipes.query.filter_by(id=post_id).first()
    send_recipe_data = {'title': recipe.title,
                        'created_by': recipe.user.username,
                        'creator_id': recipe.user.id,
                        'creator_avatar': recipe.user.provider_pic,
                        'post_id': recipe.id,
                        'description': recipe.description,
                        'imgUrl': recipe.imgUrl,
                        'date_created': recipe.date_created,
                        'ingredients': [{'ingredient': j.ingredient,
                                         'quantity': j.quantity} for j in Ingredients.query.filter(Ingredients.recipe_id == recipe.id).all()],
                        'instructions': [k.instruction for k in Instructions.query.filter(Instructions.recipe_id == recipe.id).all()],
                        'comments': [{'comment': l.comment, 'user': l.user.username} for l in Comments.query.filter(Comments.post_id == recipe.id).all()],
                        }
    return jsonify(send_recipe_data)


# @app.route('/getuserrecipe', methods=['GET'])
# @login_required
# def getuserrecipe():
#     #  user = Users.query.filter_by(id=current_user.id).first()
#     recipedata = Recipes.query.with_entities(
#         Recipes.id, Recipes.title, Recipes.description, Recipes.date_created).filter_by(user_id=current_user.id).all()
#     sending = {'user_id': current_user.id,
#                "user_recipes": [{'recipe_id': i.id,
#                                  'title': i.title,
#                                  'description': i.description,
#                                  'date_created': i.date_created,
#                                  'ingredients': [j.ingredient for j in Ingredients.query.filter(Ingredients.recipe_id == i.id).all()],
#                                  'instructions': [k.instruction for k in Instructions.query.filter(Instructions.recipe_id == i.id).all()],
#                                  'liked': check_liked(recipe_id=i.id)
#                                  } for i in recipedata]}
#     return jsonify(sending)


@app.route('/test_user')
@login_required
def test_user():
    # logout_user()
    user = current_user
    print('============', current_user.id)

    return jsonify({'user': 'ok'})


@app.route('/postliked', methods=['GET', 'POST'])
@login_required
def isliked():
    data = request.get_json()
    print('========', data)
    if request.method == 'POST':
        check_like = isLikes.query.filter_by(
            user_id=current_user.id, post_id=data['post_id']).first()
        if not check_like:
            liked = isLikes(user_id=current_user.id,
                            post_id=data['post_id'],
                            is_liked=data['is_liked']
                            )
            db.session.add(liked)
        elif check_like:
            check_like.is_liked = data['is_liked']
        db.session.commit()
    likes = isLikes.query.filter_by(
        post_id=data['post_id'], is_liked=True).all()
    total_likes = len(likes)
    sendData = {'is_liked': data['is_liked'],
                'count': total_likes,
                'post_id': data['post_id'],
                "users": [{
                    "name": i.user.name,
                    "username": i.user.username} for i in likes]}
    return jsonify(sendData)


@app.route('/usersubscribe', methods=['POST'])
@login_required
def usersubscribe():
    data = request.get_json()
    # if request.method == 'POST':
    subscriber = Users.query.filter_by(id=current_user.id).first()
    user_subscribed = Users.query.filter_by(
        id=data['user_subscribed']).first()
    check_subscribe = Subscribe.query.filter_by(
        subscriber=current_user.id, user_subscribed=data['user_subscribed']).first()
    if not check_subscribe:
        is_subscribed = Subscribe(is_subscribed=True)
        is_subscribed.user_subscribed = user_subscribed.id
        is_subscribed.subscriber = subscriber.id
        subscriber.subscriber.append(is_subscribed)
        db.session.commit()
    elif check_subscribe:
        check_subscribe.is_subscribed = not check_subscribe.is_subscribed
    db.session.commit()
    return jsonify({'success': 'true'})


@app.route('/issubscribed', methods=['POST', 'GET'])
@login_required
def issubscribed():
    data = request.get_json()
    is_subscribed = Subscribe.query.filter_by(
        subscriber=current_user.id, user_subscribed=data['user_subscribed']).first()
    return jsonify({'is_subscribed': is_subscribed.is_subscribed})


@app.route('/postuserphoto', methods=['POST'])
@login_required
def postuserphoto():
    data = request.get_json()
    user = Users.query.filter_by(id=current_user.id).first()
    if data['provider_pic'] != '':
        user.provider_pic = data['provider_pic']
        db.session.commit()
    return jsonify({'success': "true"})


@app.route('/postcomment', methods=['POST', 'GET'])
@login_required
def postcomment():
    data = request.get_json()
    print('========', data)
    post = Recipes.query.filter_by(id=data['post_id']).first()
    if request.method == 'POST':
        comment = Comments(comment=data['comment'],
                           date_posted=datetime.now())
        post.comments.append(comment)
        current_user.comments.append(comment)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'success': 'true'})
    return jsonify({'success': 'false'})


if (__name__) == '__main__':
    app.run(debug=True)
