import os
import sys
import tempfile
import pytest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models.ecommerce.models import Product

@pytest.fixture(scope='module')
def test_app():
    """Create and configure a new app instance for testing."""
    # Create a temporary file for the database
    db_fd, db_path = tempfile.mkstemp()
    
    # Create a test config
    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
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
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='module')
def client(test_app):
    """A test client for the app."""
    return test_app.test_client()

@pytest.fixture(scope='module')
def runner(test_app):
    """A test runner for the app's Click commands."""
    return test_app.test_cli_runner()

@pytest.fixture(scope='function')
def init_database(test_app):
    """Initialize the database with test data."""
    with test_app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create test products
        products = [
            Product(
                title=f'Test Product {i}',
                description=f'Test Description {i}',
                price=9.99 + i,
                image=f'test{i}.jpg',
                category=f'category{i % 3}',
                rating_rate=4.0 + (i * 0.1),
                rating_count=10 + i
            ) for i in range(1, 6)
        ]
        
        db.session.add_all(products)
        db.session.commit()
    
    yield db  # this is where the testing happens
    
    # Clean up after testing
    with test_app.app_context():
        db.session.remove()
        db.drop_all()
