# -*- coding:utf-8 -*-


from celery import Celery
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from api.lib.utils import ESHandler
# from api.lib.utils import RedisHandler

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
celery = Celery()
cors = CORS(supports_credentials=True)
# rd = RedisHandler()
# es = ESHandler()

# flask-login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'LoginView'