import os
import sys
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models.ecommerce.models import db, Product

@pytest.fixture(scope='module')
def test_app():
    """Create and configure a new app instance for testing."""
    # Create a test config
    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        WTF_CSRF_ENABLED = False
    
    # Create the app with test config
    app = create_app()
    app.config.from_object(TestConfig)
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
        
    yield app
    
    # Clean up after testing
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_database_connection(test_app):
    """Test database connection and table creation."""
    with test_app.app_context():
        # Check if we can connect to the database
        engine = db.engine
        connection = engine.connect()
        assert connection is not None, "Failed to connect to the database"
        
        # Check if tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert 'product' in tables, "Product table does not exist"
        
        # Check product table columns
        columns = {col['name']: col['type'].__class__.__name__ for col in inspector.get_columns('product')}
        expected_columns = [
            'id', 'title', 'description', 'price', 
            'image', 'category', 'rating_rate', 'rating_count'
        ]
        
        for col in expected_columns:
            assert col in columns, f"Column {col} is missing from the product table"
            
        connection.close()

def test_product_model(test_app):
    """Test Product model functionality."""
    with test_app.app_context():
        # Create a test product
        product = Product(
            title='Test Product',
            description='A test product',
            price=9.99,
            image='test.jpg',
            category='test',
            rating_rate=4.5,
            rating_count=100
        )
        
        db.session.add(product)
        db.session.commit()
        
        # Test if product was added
        assert product.id is not None, "Product ID should be generated"
        
        # Test product retrieval
        retrieved = Product.query.first()
        assert retrieved is not None, "Should be able to retrieve the product"
        assert retrieved.title == 'Test Product', "Product title doesn't match"
        assert retrieved.price == 9.99, "Product price doesn't match"
