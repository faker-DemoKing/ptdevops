# -*- coding:utf-8 -*-

import os

from flask import Blueprint
from flask_restful import Api

from api.resource import register_resources
from api.views.account import LoginView, LogoutView

HERE = os.path.abspath(os.path.dirname(__file__))

# account
blueprint_account = Blueprint('account_api', __name__, url_prefix='/api')
account_rest = Api(blueprint_account)
account_rest.add_resource(LoginView, LoginView.url_prefix)
account_rest.add_resource(LogoutView, LogoutView.url_prefix)

# user
blueprint_user_v1 = Blueprint('user_api_v1', __name__, url_prefix='/api/v1/user')
user_rest = Api(blueprint_user_v1)
register_resources(os.path.join(HERE, "user"), user_rest)

# home
blueprint_home_v1 = Blueprint('home_api_v1', __name__, url_prefix='/api/v1/home')
home_rest = Api(blueprint_home_v1)
register_resources(os.path.join(HERE, "home"), home_rest)

# host
blueprint_host_v1 = Blueprint('host_api_v1', __name__, url_prefix='/api/v1/host')
host_rest = Api(blueprint_host_v1)
register_resources(os.path.join(HERE, "host"), host_rest)
