from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import Transaction, db
from app.schemas import transaction_schema, transactions_schema
from app.utils.util import token_required


transaction_bp = Blueprint('transaction_bp', __name__, url_prefix='/transactions')


@transaction_bp.route("/", methods=['POST'])
@token_required
def create_transaction():
    try:
        transaction_data = transaction_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_transaction = Transaction(**transaction_data)
    db.session.add(new_transaction)
    db.session.commit()
    return transaction_schema.jsonify(new_transaction), 201


@transaction_bp.route("/<int:transaction_id>", methods=['GET'])
@token_required
def get_transaction(transaction_id):
    transaction = db.session.get(Transaction, transaction_id)
    if transaction is None:
        return jsonify({"message": "Transaction not found"}), 404
    return transaction_schema.jsonify(transaction), 200


@transaction_bp.route("/<int:transaction_id>", methods=['PUT'])
@token_required
def update_transaction(transaction_id):
    transaction = db.session.get(Transaction, transaction_id)
    if transaction is None:
        return jsonify({"message": "Transaction not found"}), 404

    try:
        transaction_data = transaction_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in transaction_data.items():
        if value:
            setattr(transaction, field, value)

    db.session.commit()
    return transaction_schema.jsonify(transaction), 200


@transaction_bp.route("/<int:transaction_id>", methods=['DELETE'])
@token_required
def delete_transaction(transaction_id):
    transaction = db.session.get(Transaction, transaction_id)
    if transaction is None:
        return jsonify({"message": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": f"Transaction ID {transaction_id} has been deleted"}), 200
