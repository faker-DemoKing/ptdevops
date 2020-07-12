# -*- coding:utf-8 -*- 


from __future__ import unicode_literals

from functools import wraps

import jwt
from flask import request, abort
from flask import current_app
from flask import session
from flask_login import login_user, current_user
from flask import g

from api.models.account import User
from api.libs.cache import UserCache

def _auth_with_session():
    # session 判断函数
    if isinstance(getattr(g, 'user', None), User):
        login_user(g.user)
        return True
    if "user" in session and "username" in (session["user"] or {}):
        login_user(UserCache.get(session["user"]["username"]))
        return True
    return False

def _auth_with_key():
    key = request.values.get('_key')
    secret = request.values.get('_secret')
    path = request.path
    keys = sorted(request.values.keys())
    req_args = [request.values[k] for k in keys if k not in ("_key", "_secret")]
    user, authenticated = User.query.authenticate_with_key(key, secret, req_args, path)
    if user and authenticated:
        login_user(user)
        return True
    return False

def _auth_with_token():
    auth_headers = request.headers.get('Access-Token', '').strip()
    if not auth_headers:
        return False

    try:
        token = auth_headers
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.filter_by(email=data['sub']).first()
        if not user:
            return False

        login_user(user)
        g.user = user
        return True
    except jwt.ExpiredSignatureError:
        return False
    except (jwt.InvalidTokenError, Exception):
        return False

def auth_required(func):
    if request.json is not None:
        setattr(request, 'values', request.json)
    else:
        setattr(request, 'values', request.values.to_dict())

    current_app.logger.debug(request.values)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            # 先判断有没有authenticated这个属性是否为True，是的话表示通过认证
            return func(*args, **kwargs)
        if _auth_with_session():
            return func(*args, **kwargs)
        # 再判断session or key or token or ip_white_list，满足一样即可
        abort(401)

    return wrapper

def auth_abandoned(func):
    setattr(func, "authenticated", False)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper