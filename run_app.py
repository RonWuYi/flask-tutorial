import os

os.system('export FLASK_APP = flaskr/__init__.py:create_app')
os.system('export FLASK_ENV = development')
os.system('export FLASK_DEBUG = 0')
os.system('flask run')