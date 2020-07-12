# -*- coding:utf-8 -*-

import os
import sys
from inspect import getmembers, isclass

import six
import json
from flask import jsonify, Response, jsonify
from flask_restful import Resource
from flask_sqlalchemy import BaseQuery

from api.libs.perm import auth_required
from api.libs.utils import AttrDict, DateTimeEncoder

# 视图继承类
class APIView(Resource):
    method_decorators = [auth_required]  # 进来之前要先执行的认证函数

    def __init__(self):
        super(APIView, self).__init__()

    @staticmethod
    def jsonify(data='', error=''):
        content = AttrDict(data=data, error=error)

        if error:
            content.data = ''
        elif hasattr(data, 'to_dict'):
            content.data = data.to_dict()
        elif isinstance(data, (list, BaseQuery)) and all([hasattr(item, 'to_dict') for item in data]):
            content.data = [item.to_dict() for item in data]
        return jsonify(content)
        # return Response(json.dumps(content, cls=DateTimeEncoder), content_type='application/json')
        
API_PACKAGE = "api"

def register_resources(resource_path, rest_api): # 注册路由，通过被调用的方式
    for root, _, files in os.walk(os.path.join(resource_path)):
        for filename in files:
            if not filename.startswith("_") and filename.endswith("py"):
                module_path = os.path.join(API_PACKAGE, root[root.index("views"):])
                if module_path not in sys.path:
                    sys.path.insert(1, module_path)
                view = __import__(os.path.splitext(filename)[0])
                resource_list = [o[0] for o in getmembers(view) if isclass(o[1]) and issubclass(o[1], Resource)]
                resource_list = [i for i in resource_list if i != "APIView"]
                for resource_cls_name in resource_list:
                    resource_cls = getattr(view, resource_cls_name)
                    if not hasattr(resource_cls, "url_prefix"):
                        resource_cls.url_prefix = ("",)
                    if isinstance(resource_cls.url_prefix, six.string_types):
                        resource_cls.url_prefix = (resource_cls.url_prefix,)

                    rest_api.add_resource(resource_cls, *resource_cls.url_prefix)