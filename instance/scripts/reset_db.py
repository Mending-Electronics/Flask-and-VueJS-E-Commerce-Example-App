import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))

from app import create_app, db
from models.ecommerce.models import Product
from instance.scripts.seed_db import seed_database

def reset_database():
    """Reset the database by dropping all tables and reseeding with sample data."""
    print("Resetting database...")
    
    # Initialize Flask app
    app = create_app()
    
    with app.app_context():
        # Get database info before reset
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"Database URI: {db_uri}")
        
        if 'sqlite' in db_uri and not app.config.get('TESTING', False):
            db_path = db_uri.replace('sqlite:///', '')
            print(f"Database will be reset at: {os.path.abspath(db_path)}")
            
            # Ask for confirmation if not in testing mode
            if not app.config.get('TESTING', False):
                confirm = input("\nWARNING: This will delete all data in the database. Continue? (y/n): ")
                if confirm.lower() != 'y':
                    print("Operation cancelled.")
                    return False
        
        # Drop all tables
        print("\nDropping all tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Seed the database
        print("Seeding database with sample data...")
        if seed_database(app):
            # Verify data was added
            product_count = Product.query.count()
            categories = [c[0] for c in db.session.query(Product.category).distinct().all() if c[0]]
            
            print(f"\nDatabase reset and seeded successfully!")
            print(f"- Added {product_count} products")
            print(f"- Categories: {', '.join(categories) if categories else 'None'}")
            
            return True
        else:
            print("Error seeding database!")
            return False

def create_test_database():
    """Create a test database with sample data for testing purposes."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database(app)
        
        # Verify
        product_count = Product.query.count()
        print(f"Created test database with {product_count} products")

if __name__ == '__main__':
    reset_database()
