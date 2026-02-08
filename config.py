import os
from app import app

# For Render deployment, DATABASE_URL is automatically provided if a DB is linked.
# If not, we fall back to a local sqlite database for safety.
db_url = os.getenv('DATABASE_URL', 'sqlite:///database.db')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key_change_me_in_production')
