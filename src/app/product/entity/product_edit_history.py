from src.core.database import db
from datetime import datetime
from enum import Enum

class EditAction(Enum):
    CREATE = 'create'
    DELETE = 'delete'
    UPDATE = 'update'

class ProductEditHistory(db.Model):
    __tablename__ = 'product_edit_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.Enum(EditAction), nullable=False)
    product = db.relationship('Product', backref='edit_history')
    user = db.relationship('User', backref='edit_history')

    def to_dict(self):
        
        return {
            "id": self.id,
            "createdAt": self.created_at.isoformat(),
            "product": self.product_id,
            "user": self.user_id,
            "action": self.action.value
        }
