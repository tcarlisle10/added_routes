from app.models import Transaction
from app.extensions import ma


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        include_fk = True

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)