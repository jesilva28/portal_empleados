import os
from decouple import config
import secrets

basedir= os.path.abspath(os.path.dirname(__file__))
class Config():
    
    CSRF_ENABLE = True
    SECRET_KEY = config('SECRET_KEY',secrets.token_urlsafe(64))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"


 