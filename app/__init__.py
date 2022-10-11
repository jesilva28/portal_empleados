import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_navigation import Navigation
from flask_session import Session

#Almacenar en la variable basedir la ruta donde va estar mi bd

basedir= os.path.abspath(os.path.dirname(__file__))

app= Flask(__name__)

app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
bc = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)
nav = Navigation(app)
session = Session(app)

@app.before_first_request
def initialize_db():
    db.create_all()

from app import modelos, rutas 




