from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DEBUG = 'True'
SECRET_KEY = 'secretkey'

#UPLOAD FOLDER
UPLOAD_FOLDER = "./app/static/uploads"

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project1:password123@localhost/project1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)
from app import views