# Flask Vue E-commerce

A simple e-commerce application built with Flask and Vue.js.

## Features

- Product catalog with categories
- Shopping cart functionality
- Responsive design with Bootstrap
- RESTful API backend
- SQLite database with Flask-SQLAlchemy
- Database migrations with Flask-Migrate
- Unit and integration tests with pytest
- Responsive grid layout
- Product search functionality

### Shopping Cart
- Add/remove items from cart
- Update quantities in real-time
- Cart persistence across sessions
- Order summary with subtotal

### User Experience
- Clean, modern UI with Bootstrap 5
- Responsive design works on all devices
- Smooth page transitions
- Real-time updates without page reloads

## Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database (included with Python)
- **Flask-Bootstrap** - For quick UI scaffolding

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Axios** - For making HTTP requests
- **Bootstrap 5** - For responsive design and components
- **Font Awesome** - For icons

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Flask-Vue-Sample-App/src
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

```
src/
├── instance/               # Database and instance-specific files
├── static/
│   └── js/
│       ├── catalog.js     # Vue application for catalog page
│       └── cart.js        # Vue application for cart page
├── templates/
│   ├── base.html          # Base template with common layout
│   ├── catalog.html       # Product catalog page
│   └── cart.html          # Shopping cart page
├── app.py                # Main Flask application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## API Endpoints

- `GET /api/products` - Get all products
- `GET /api/cart` - Get cart contents
- `POST /api/cart` - Update cart (add/remove/set quantity)
  - Parameters: `product_id`, `action` (add/remove/set), `quantity` (for 'set' action)

## Database

The application uses SQLite for simplicity. The database file (`ecommerce.db`) will be automatically created in the `instance` folder when you first run the application. It will be populated with sample products from the [FakeStore API](https://fakestoreapi.com/).

## Customization

### Adding New Features
1. Add new routes in `app.py`
2. Create new Vue components in `static/js/`
3. Add new templates in the `templates/` directory

### Styling
- The application uses Bootstrap 5 for styling
- Custom CSS can be added in the `<style>` blocks of each template
- For component-specific styles, consider using scoped styles in Vue components

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [FakeStore API](https://fakestoreapi.com/) for sample product data
- [Bootstrap 5](https://getbootstrap.com/) for the responsive design framework
- [Vue.js](https://vuejs.org/) for the reactive frontend framework