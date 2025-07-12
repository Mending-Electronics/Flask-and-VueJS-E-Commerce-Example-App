import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app

def check_database():
    """Check the database status and contents."""
    app = create_app()
    with app.app_context():
        # Get database path from config
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            db_path = os.path.abspath(db_path)
        else:
            db_path = db_uri
            
        print(f"Database URI: {db_uri}")
        print(f"Database path: {db_path}")
        print(f"Database exists: {os.path.exists(db_path) if db_uri.startswith('sqlite') else 'N/A (not SQLite)'}")
        
        try:
            # Check if we can connect to the database
            engine = db.engine
            connection = engine.connect()
            print("\nSuccessfully connected to the database!")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"\nTables in database: {tables}")
            
            if 'product' in tables:
                print("\nProduct table columns:")
                columns = inspector.get_columns('product')
                for column in columns:
                    print(f"- {column['name']} ({column['type']})")
                
                # Count products
                product_count = Product.query.count()
                print(f"\nNumber of products in database: {product_count}")
                
                # Show some sample categories
                if product_count > 0:
                    categories = db.session.query(Product.category).distinct().all()
                    print("\nCategories in database:")
                    for cat in categories:  # Show all categories
                        print(f"- {cat[0] if cat[0] else '(empty)'}")
                    
                    # Show sample products
                    print("\nSample products:")
                    for i, product in enumerate(Product.query.limit(3).all(), 1):
                        print(f"{i}. {product.title} (${product.price:.2f}) - {product.category}")
            
            connection.close()
            
        except Exception as e:
            print(f"\nError accessing database: {e}")
            return False
        
        return True

if __name__ == '__main__':
    print("Checking database...")
    check_database()
