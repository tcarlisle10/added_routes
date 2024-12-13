from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import Listing, db
from app.schemas import listing_schema, listings_schema
from app.utils.util import token_required


listing_bp = Blueprint('listing_bp', __name__, url_prefix='/listings')



@listing_bp.route("/", methods=['POST'])
@token_required
def create_listing():
    try:
        listing_data = listing_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_listing = Listing(**listing_data)
    db.session.add(new_listing)
    db.session.commit()
    return listing_schema.jsonify(new_listing), 201


@listing_bp.route("/", methods=['GET'])
def get_listings():
    listings = db.session.query(Listing).all()
    return listings_schema.jsonify(listings), 200


@listing_bp.route("/<int:listing_id>", methods=['GET'])
def get_listing(listing_id):
    listing = db.session.get(Listing, listing_id)
    if listing is None:
        return jsonify({"message": "Listing not found"}), 404
    return listing_schema.jsonify(listing), 200


@listing_bp.route("/<int:listing_id>", methods=['PUT'])
@token_required
def update_listing(listing_id):
    listing = db.session.get(Listing, listing_id)
    if listing is None:
        return jsonify({"message": "Listing not found"}), 404

    try:
        listing_data = listing_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in listing_data.items():
        if value:
            setattr(listing, field, value)

    db.session.commit()
    return listing_schema.jsonify(listing), 200


@listing_bp.route("/<int:listing_id>", methods=['DELETE'])
@token_required
def delete_listing(listing_id):
    listing = db.session.get(Listing, listing_id)
    if listing is None:
        return jsonify({"message": "Listing not found"}), 404

    db.session.delete(listing)
    db.session.commit()
    return jsonify({"message": f"Listing ID {listing_id} has been deleted"}), 200
