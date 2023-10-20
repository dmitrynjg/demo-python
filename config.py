import os

database_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp')

if not os.path.exists(database_dir):
    os.makedirs(database_dir)

database_file = os.path.join(database_dir,  'database.db')

class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + database_file