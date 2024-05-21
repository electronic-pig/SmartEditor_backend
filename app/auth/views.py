from flask import jsonify, request, session

from . import auth
from .models import Users
from .. import db


@auth.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = Users(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'})


@auth.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = Users.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'username': user.username, 'email': user.email})


@auth.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = Users.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated'})


@auth.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if Users.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    new_user = Users(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Users.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 400
    session['user_id'] = user.id
    return jsonify({'message': 'User logged in'}), 200
