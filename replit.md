# Groceri - Online Grocery Store

## Overview

Groceri is a Flask-based web application for an online grocery store. It supports two user roles: regular customers who can browse products, manage a shopping cart, and place orders; and admin users who can manage product categories and products. The app uses server-side rendering with Jinja2 templates and a PostgreSQL database via SQLAlchemy ORM.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Structure

The app follows a simple flat structure with circular imports between modules:

- **`app.py`** - Creates the Flask app instance and imports config, models, and routes
- **`config.py`** - Loads configuration from environment variables (database URL, secret key)
- **`models.py`** - Defines SQLAlchemy database models and initializes the `db` object
- **`routes.py`** - Contains all route handlers, decorators for auth/admin, and business logic
- **`templates/`** - Jinja2 HTML templates using Bootstrap 5 and Font Awesome

**Important note about circular imports:** The app uses a circular import pattern where `app.py` creates the Flask instance, then `config.py`, `models.py`, and `routes.py` all import `app` from `app.py`. This is intentional but fragile — be careful when restructuring.

### Database Models

The app uses Flask-SQLAlchemy with PostgreSQL. Models defined in `models.py`:

- **User** - `id`, `username`, `passhash`, `name`, `is_admin`. Password hashing via Werkzeug.
- **Product** - `id`, `name`, `category_id` (FK to Category), `quantity`, `price`, `man_date`
- **Category** - `id`, `name`. Has one-to-many relationship with Products.
- **Cart** - Only `id` column defined; incomplete model. Referenced in routes but needs `user_id`, `product_id`, `quantity` columns.
- **Order** - Referenced in routes and templates but NOT defined in `models.py`. Needs to be created.
- **Transaction** - Referenced in routes and templates but NOT defined in `models.py`. Needs to be created.

### Incomplete/Missing Pieces

The codebase is **incomplete** and has several issues that need attention:

1. **Missing models**: `Order` and `Transaction` are imported in `routes.py` but not defined in `models.py`. The `Cart` model is only partially defined (just has an `id` column).
2. **Incomplete routes**: `routes.py` is truncated — the `profile_post` route is cut off, and many routes referenced in templates (like `add_category`, `edit_category`, `delete_category`, `show_category`, `add_product`, `edit_product`, `delete_product`, `add_to_cart`, `delete_from_cart`, `place_order`, `cart`, `orders`, `login`, `register`, `logout`, `index`) are not in the provided file.
3. **Template issues**: Some templates have unclosed HTML tags and incomplete code (truncated files).

### Authentication & Authorization

- Session-based authentication using Flask's built-in `session`
- Two custom decorators in `routes.py`: `@auth_required` (checks for `user_id` in session) and `@admin_required` (checks both login and `is_admin` flag)
- Password hashing uses Werkzeug's `generate_password_hash` / `check_password_hash`

### Frontend

- Server-side rendered with Jinja2 templates
- Base layout in `templates/layout.html` with Bootstrap 5 (CDN) and Font Awesome icons
- Template inheritance pattern: all pages extend `layout.html`
- Flash messages displayed with Bootstrap alerts (success/danger styling based on message content)
- Templates organized with category and product CRUD templates in subdirectories (`templates/category/`, `templates/product/`)

### Database Configuration

The database URL is read from `DATABASE_URL` environment variable (falling back to `SQLALCHEMY_DATABASE_URI`). It includes a `postgres://` to `postgresql://` replacement for Heroku-style URLs. The app expects a PostgreSQL database — `psycopg2-binary` is listed as a dependency.

## External Dependencies

- **PostgreSQL** - Primary database (via `psycopg2-binary` driver)
- **Flask 2.3.2** - Web framework
- **Flask-SQLAlchemy 3.0.5** - ORM integration
- **Flask-RESTful 0.3.10** - Listed in requirements but not actively used in visible code
- **Bootstrap 5.3.1** - Frontend CSS/JS framework (loaded from CDN)
- **Font Awesome 6.4.2** - Icon library (loaded from CDN)
- **Gunicorn** - Production WSGI server
- **python-dotenv** - Environment variable loading from `.env` files

### Required Environment Variables

- `DATABASE_URL` or `SQLALCHEMY_DATABASE_URI` - PostgreSQL connection string
- `SECRET_KEY` - Flask session secret key (defaults to `'default_secret_key'`)