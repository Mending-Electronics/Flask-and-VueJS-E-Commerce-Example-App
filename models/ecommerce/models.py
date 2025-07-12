from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(300), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    rating_rate = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'image': self.image,
            'category': self.category,
            'rating': {
                'rate': self.rating_rate,
                'count': self.rating_count
            }
        }

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    # Relationship
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product': {
                'id': self.product.id,
                'title': self.product.title,
                'price': self.product.price,
                'image': self.product.image
            },
            'total_price': self.quantity * self.product.price
        }
