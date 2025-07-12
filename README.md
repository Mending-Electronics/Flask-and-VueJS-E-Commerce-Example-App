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
   cd Flask-and-VueJS-E-Commerce-Example-App/src
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
│   └── components/
│       ├── catalog.vue     # Vue application for catalog page
│       └── cart.vue        # Vue application for cart page
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
2. Create new Vue components in `static/components/`
3. Add new templates in the `templates/` directory

### Styling
- The application uses Bootstrap 5 for styling
- Custom CSS can be added in the `<style>` blocks of each template
- For component-specific styles, consider using scoped styles in Vue components

## Acknowledgments

### APIs (to enrich the db with fake data)
- [FakeStore API](https://fakestoreapi.com/) for sample product data

### Frontend
- [Bootstrap 5](https://getbootstrap.com/) for the responsive design framework
- [Vue.js](https://vuejs.org/) for the reactive frontend framework
- [Axios](https://axios-http.com/) for making HTTP requests to the backend

### Backend
- [Flask](https://flask.palletsprojects.com/) for the backend framework
-  [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/) for handling CORS (backend security)
- [WTForms](https://wtforms.readthedocs.io/en/stable/) for form secure handling
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) for database operations (ORM)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) for database migrations (versionning)
- [loguru](https://loguru.readthedocs.io/en/stable/) for logging
- [requests](https://requests.readthedocs.io/en/latest/) for making HTTP requests
- [pytest](https://docs.pytest.org/en/stable/) for testing
- [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) for code coverage
- [python-dotenv](https://pypi.org/project/python-dotenv/) for environment variables







## 🧱 Comparaison des stacks : Flask + Vue.js vs Django + Coton

## ⚙️ Matrice de choix des technologies

| Catégorie / Critère                  | **Flask + Vue.js + Bootstrap5 (Votre stack)**                                                                 | **Django + Coton + AlpineJS + HTMX**                                                   |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| **🧠 Framework backend**            | ✅ Flask – léger, modulaire, configuration minimale                                                            | ✅ Django – complet, avec de nombreuses fonctionnalités intégrées                       |
| **🧩 Composants Back-end**          | ✅ Blueprints Flask – structure modulaire, extensible par micro-apps                                           | ✅ Django Apps – architecture modulaire, réutilisable                                   |
| **🧩 Composants Front-end**         | ✅ Vue.js – composants réactifs, manipulation DOM via hooks, ES5 sans build                                    | ✅ AlpineJS – composants légers, déclaratifs, sans compilation                          |
| **🎨 Framework CSS**                | ✅ Bootstrap 5 – responsive, populaire, intégré via CDN                                                        | ✅ Coton – basé sur TailwindCSS, design opinié                                          |
| **🔄 Requêtes (HTTP)**              | ✅ Axios – client HTTP basé sur Promises, gestion des erreurs, JSON auto, CDN                                 | ✅ HTMX – AJAX déclaratif via attributs HTML, pas de JS requis                          |
| **🔧 Processus de build**           | ✅ Aucun – Vue utilisé directement en JavaScript ES5 via CDN                                                   | ✅ Aucun – AlpineJS et HTMX intégrés directement sans compilation                       |
| **🔁 Flux de données**             | ✅ API REST – Flask poste les données, Vue les récupère via Axios                                              | ⚠️ Piloté par le serveur – HTMX récupère des fragments HTML, Alpine gère la logique    |
| **🗃️ ORM intégré**                | ✅ SQLAlchemy – ORM puissant, support multi-bases (ex: `users.db`, `orders.db`)                                | ✅ Django ORM – intégré, mais ❌ ne supporte pas les bases NoSQL nativement             |
| **🧪 Migration de base de données** | ✅ Flask-Migrate – basé sur Alembic, versionnage et évolution du schéma                                        | ✅ Django Migrations – système intégré, robuste                                         |
| **🧬 Support NoSQL**               | ✅ Compatible avec MongoDB, Cassandra, Redis via extensions                                                    | ❌ Non pris en charge officiellement                                                    |
| **🔐 Sécurité**                     | ✅ Flask avec en-têtes sécurisées et gestion des routes                                                        | ✅ Django intègre sécurité CSRF, authentification, permissions                          |
| **📚 Courbe d’apprentissage**       | ⚠️ Moyenne – Flask et Vue sont simples mais nécessitent de l’intégration                                       | ⚠️ Plus raide – ORM Django, HTMX et Alpine nécessitent la compréhension du backend     |
| **🚀 Performance**                  | ✅ Rapide – JS minimal, chargement via CDN, appels asynchrones API                                             | ✅ Rapide – peu de JS, rendus serveur efficaces                                         |
| **🎯 Cas d’usage idéal**           | ✅ Applications pilotées par API, dashboards, e-commerce, interface agile                                      | ✅ Interfaces CRUD, panneaux d’administration, sites de contenu                         |
| **🌍 Communauté / Écosystème**      | ✅ Large – Forte communauté pour Flask et Vue                                                                  | ✅ Écosystème mature pour Django ; HTMX et AlpineJS en pleine croissance                |
| **📦 Déploiement**                  | ✅ Simple – Flask facilement conteneurisé, Vue servi statiquement                                              | ⚠️ Déploiement Django nécessite configuration, mais inclut admin, ORM, etc.    

## Tips

> Qu'est ce qu'un CDN ?

> Pourquoi privilegier un framework frontend et un framework backend ?

> La Syntaxe Moustache commune au moteur de Template Jinja et Vue comment integrer des compossant vue dans un template Jinja ?


> Genrer les logs


> Gerer les migration de bases de données




## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.