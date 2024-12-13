from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import Skill, db
from app.schemas import skill_schema, skills_schema
from app.utils.util import token_required

skill_bp = Blueprint('skill_bp', __name__, url_prefix='/skills')

@skill_bp.route("/", methods=['POST'])
@token_required
def create_skill():
    try:
        skill_data = skill_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_skill = Skill(**skill_data)
    db.session.add(new_skill)
    db.session.commit()
    return skill_schema.jsonify(new_skill), 201


@skill_bp.route("/", methods=['GET'])
def get_skills():
    skills = db.session.query(Skill).all()
    return skills_schema.jsonify(skills), 200


@skill_bp.route("/<int:skill_id>", methods=['GET'])
def get_skill(skill_id):
    skill = db.session.get(Skill, skill_id)
    if skill is None:
        return jsonify({"message": "Skill not found"}), 404
    return skill_schema.jsonify(skill), 200


@skill_bp.route("/<int:skill_id>", methods=['PUT'])
@token_required
def update_skill(skill_id):
    skill = db.session.get(Skill, skill_id)
    if skill is None:
        return jsonify({"message": "Skill not found"}), 404

    try:
        skill_data = skill_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in skill_data.items():
        if value:
            setattr(skill, field, value)

    db.session.commit()
    return skill_schema.jsonify(skill), 200


@skill_bp.route("/<int:skill_id>", methods=['DELETE'])
@token_required
def delete_skill(skill_id):
    skill = db.session.get(Skill, skill_id)
    if skill is None:
        return jsonify({"message": "Skill not found"}), 404

    db.session.delete(skill)
    db.session.commit()
    return jsonify({"message": f"Skill ID {skill_id} has been deleted"}), 200
