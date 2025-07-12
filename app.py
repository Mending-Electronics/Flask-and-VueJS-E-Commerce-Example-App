import os
from pathlib import Path
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, send_from_directory
from flask_bootstrap import Bootstrap5
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from config import Config
from models.ecommerce.models import db, Product, CartItem
from models.ecommerce.forms import CheckoutForm
from instance.scripts.seed_db import seed_database
from logging_config import configure_logging


# Load environment variables
load_dotenv()

# Initialize extensions
bootstrap = Bootstrap5()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    """Application factory function."""
    # Set base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set template and static folders
    ecommerce_template_dir = os.path.join(base_dir, 'models', 'ecommerce', 'templates')
    root_template_dir = os.path.join(base_dir, 'templates')
    
    # Set static folder to be in the root static directory
    static_dir = os.path.join(base_dir, 'static')
    ecommerce_static_dir = os.path.join(base_dir, 'models', 'ecommerce', 'static')
    
    # Create app with template and static folders
    app = Flask(__name__, 
                template_folder=ecommerce_template_dir,
                static_folder=static_dir)
    
    # Add root template directory to template loader
    app.jinja_loader.searchpath.append(root_template_dir)
    
    # Create a route to serve static files from the ecommerce static directory
    @app.route('/static/ecommerce/<path:filename>')
    def ecommerce_static(filename):
        return send_from_directory(os.path.join(ecommerce_static_dir), filename)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Enable debug mode if FLASK_DEBUG is set
    if os.environ.get('FLASK_DEBUG') == '1':
        app.config['DEBUG'] = True
    
    # Configure Bootstrap with Flatly theme
    app.config['BOOTSTRAP_SERVE_LOCAL'] = False
    app.config['BOOTSTRAP_CDN_FORCE_SSL'] = True
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'flatly'
   

    # Initialize configuration
    if hasattr(config_class, 'init_app'):
        config_class.init_app(app)
    
    # Initialize extensions
    bootstrap.init_app(app)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure logging
    logger = configure_logging(app)
    app.logger = logger  # Make logger available via app.logger
    
    # Log application startup
    logger.info("=" * 50)
    logger.info("Application starting...")
    logger.info(f"Environment: {app.config.get('FLASK_ENV', 'production')}")
    logger.info(f"Debug mode: {app.debug}")
    logger.info(f"Database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    logger.info(f"Log level: {app.config.get('LOG_LEVEL', 'INFO')}")
    logger.info("=" * 50)
    
        # Register blueprints here (if any)
    # from .api import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f'Not found error: {error}')
        return jsonify({
            'status': 'error',
            'message': 'Resource not found',
            'error': str(error)
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal server error: {error}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'error': str(error) if app.debug else 'An internal error occurred'
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled exception: {error}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'error': str(error) if app.debug else 'Internal server error'
        }), 500
    
    return app

# Create app instance
app = create_app()


# Initialize database
def init_db():
    """Initialize the database"""
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("Database tables created successfully.")
        
        # Seed the database if it's empty
        product_count = Product.query.count()
        print(f"Found {product_count} products in the database.")
        
        if product_count == 0:
            print("Seeding database with sample products...")
            if seed_database(app):
                print("Database seeded successfully.")
            else:
                print("Error seeding database.")
        else:
            print("Database already contains data. Skipping seeding.")

# Routes
@app.route('/')
def index():
    return render_template('ecommerce/catalog.html')

@app.route('/cart')
def cart():
    return render_template('ecommerce/cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    cart_items = CartItem.query.all()
    
    # Check if cart is empty
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart'))
    
    # Process form submission
    if form.validate_on_submit():
        try:
            # Process the order here
            # For now, we'll just show a success message
            flash('Your order has been placed successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            app.logger.error(f"Error processing order: {str(e)}")
            flash('An error occurred while processing your order. Please try again.', 'danger')
    
    # Calculate totals for the order summary
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    tax = subtotal * 0.1  # 10% tax
    total = subtotal + tax
    
    return render_template('ecommerce/checkout.html', form=form, cart_items=cart_items, subtotal=subtotal, tax=tax, total=total)

# API Routes
@app.route('/api/products')
def get_products():
    products = Product.query.all()
    result = []
    for p in products:
        result.append({
            'id': p.id,
            'title': p.title,
            'price': p.price,
            'description': p.description,
            'category': p.category,  # Make sure this matches the model field name
            'image': p.image,
            'rating': {
                'rate': p.rating_rate,
                'count': p.rating_count
            }
        })
    return jsonify(result)

@app.route('/api/cart', methods=['GET', 'POST'])
def handle_cart():
    if request.method == 'POST':
        data = request.get_json()
        product_id = data.get('product_id')
        action = data.get('action', 'add')  # 'add', 'remove', or 'set'
        
        if action == 'add':
            # Add to cart logic
            cart_item = CartItem.query.filter_by(product_id=product_id).first()
            if cart_item:
                cart_item.quantity += 1
            else:
                cart_item = CartItem(product_id=product_id)
                db.session.add(cart_item)
        elif action == 'remove':
            # Remove from cart logic
            cart_item = CartItem.query.filter_by(product_id=product_id).first()
            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                else:
                    db.session.delete(cart_item)
        elif action == 'set' and 'quantity' in data:
            # Set specific quantity
            quantity = int(data['quantity'])
            cart_item = CartItem.query.filter_by(product_id=product_id).first()
            if cart_item:
                if quantity > 0:
                    cart_item.quantity = quantity
                else:
                    db.session.delete(cart_item)
        
        db.session.commit()
    
    # Return the updated cart
    cart_items = CartItem.query.all()
    return jsonify([{
        'id': item.id,
        'product_id': item.product_id,
        'quantity': item.quantity,
        'product': {
            'id': item.product.id,
            'title': item.product.title,
            'price': item.product.price,
            'image': item.product.image
        }
    } for item in cart_items])

def create_app():
    # This function is used to create the Flask application for testing or other purposes
    return app

if __name__ == '__main__':
    # Initialize database
    with app.app_context():
        init_db()
    
    # Run the application
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)