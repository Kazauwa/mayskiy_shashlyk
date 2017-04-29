import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLALCHEMY_DATABASE_URI = os.path.join(BASE_DIR, 'fires.sqlite')
