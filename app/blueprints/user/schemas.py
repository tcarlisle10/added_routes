from app.models import User
from app.extensions import ma
from marshmallow import fields


from app.models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

    skills = fields.Nested('SkillSchema', many=True)
    listings = fields.Nested('ListingSchema', many=True)
    transactions = fields.Nested('TransactionSchema', many=True)
    reviews_given = fields.Nested('ReviewSchema', many=True)
    reviews_received = fields.Nested('ReviewSchema', many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class RatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        include_fk = True

rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        include_fk = True

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)