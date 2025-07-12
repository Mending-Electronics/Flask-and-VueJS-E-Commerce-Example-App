import sys
from pathlib import Path
import requests

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))

from models.ecommerce.models import db, Product

def seed_database(app):
    """Seed the database with products from FakeStore API."""
    print("Seeding database with products from FakeStore API...")
    
    with app.app_context():
        # Clear existing data
        db.session.query(Product).delete()
        
        try:
            # Fetch products from FakeStore API
            response = requests.get('https://fakestoreapi.com/products')
            response.raise_for_status()  # Raise an exception for bad status codes
            
            products = response.json()
            
            for product_data in products:
                product = Product(
                    id=product_data['id'],
                    title=product_data['title'],
                    description=product_data['description'],
                    price=float(product_data['price']),
                    image=product_data['image'],
                    category=product_data.get('category', 'uncategorized'),  # Add category field
                    rating_rate=float(product_data['rating']['rate']),
                    rating_count=int(product_data['rating']['count'])
                )
                db.session.add(product)
            
            db.session.commit()
            print(f"Successfully added {len(products)} products to the database.")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {str(e)}")
            return False
