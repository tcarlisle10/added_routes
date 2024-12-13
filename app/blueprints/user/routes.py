from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import User, db
from app.schemas import user_schema, users_schema
from app.utils.util import token_required
from werkzeug.security import generate_password_hash, check_password_hash


user_bp = Blueprint('user_bp', __name__, url_prefix='/users')


@user_bp.route("/", methods=['POST'])
def create_user():
    try:
        user_data = request.json
        user_data = user_schema.load(user_data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    pwhash = generate_password_hash(user_data['password'])
    new_user = User(
        name=user_data['name'],
        email=user_data['email'],
        phone=user_data['phone'],
        password=pwhash
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify("User has been added to the database."), 201


@user_bp.route("/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    return user_schema.jsonify(user), 200


@user_bp.route("/<int:user_id>", methods=['PUT'])
@token_required
def update_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in user_data.items():
        if value:
            setattr(user, field, value)

    db.session.commit()
    return user_schema.jsonify(user), 200


@user_bp.route("/<int:user_id>", methods=['DELETE'])
@token_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User ID {user_id} has been deleted"}), 200
