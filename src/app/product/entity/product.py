from src.core.database import db
from datetime import datetime
from sqlalchemy import event

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_delete = db.Column(db.Boolean, default=False, nullable=False)

    @staticmethod
    def update_timestamp(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "isDelete": self.is_delete,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

event.listen(Product, 'before_update', Product.update_timestamp)