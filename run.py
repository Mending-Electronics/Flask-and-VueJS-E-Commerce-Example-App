#!/usr/bin/env python3
"""
Run the Flask development server.
"""
import os
from app import create_app, db
from config import Config

# Create application instance
app = create_app()

if __name__ == '__main__':
    try:
        with app.app_context():
            # Create database tables if they don't exist
            db.create_all()
            
            # Check if we need to seed the database
            from models.ecommerce.models import Product
            product_count = Product.query.count()
            app.logger.info(f"Found {product_count} products in the database.")
            
            if product_count == 0:
                app.logger.info("No products found. Seeding database...")
                from instance.scripts.seed_db import seed_database
                if seed_database(app):
                    app.logger.info("Database seeded successfully.")
                else:
                    app.logger.error("Failed to seed database.")
            
            # Run the application
            app.logger.info(f"Starting server on {app.config['HOST']}:{app.config['PORT']}")
            
    except Exception as e:
        app.logger.critical(f"Failed to start application: {str(e)}", exc_info=True)
        raise
    
    # Run the application
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
