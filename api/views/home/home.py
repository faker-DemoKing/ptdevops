# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import request
from sqlalchemy import and_
import json

from api.libs import human_date
from api.resource import APIView
from api.models import App, Host, Task, Detection, Alarm, DeployRequest, Deploy

class GetStatistic(APIView):
    '''
        获取总览数据，app，host，task，detection
    '''
    url_prefix = '/statistic'

    def get(self):
        data = {
            'app': App.query.count(),
            'host': Host.query.count(),
            'task': Task.query.count(),
            'detection': Detection.query.count()
        }
        return self.jsonify(data)

class GetAlarm(APIView):
    '''
        home获取报警
    '''
    url_prefix = '/alarm'

    def get(self):
        now = datetime.now()

        data = {human_date(now - timedelta(days=x + 1)): 0 for x in range(14)}
        # 获取十四天以内的报警
        for alarm in Alarm.query.filter(and_(Alarm.status == 1, Alarm.created_at.__gt__(human_date(now - timedelta(days=14))))):
            date = alarm.created_at[:10]
            if date in data:
                data[date] += 1
        data = [{'date': k, 'value': v} for k, v in data.items()]
        return self.jsonify(data)

class GetRequest(APIView):
    '''
        deploy发布展示
    '''
    url_prefix = '/request'

    def get(self):
        data = { x.id: {'name': x.name, 'count': 0 } for x in App.query.all() }
        for req in DeployRequest.query.filter(DeployRequest.create_at.__gt__(human_date())):
            data[req.deploy.app_id]['count'] += 1
        data = sorted(data.values(), key=lambda x: x['count'], reverse=True)[:5]
        return self.jsonify(data)

class GetDeploy(APIView):
    '''
        应用部署
    '''
    url_prefix = '/deploy'

    def get(self):
        host = Host.query.filter(Host.deleted_at.is_(None)).count()
        data = { x.id: {'name': x.name, 'count': 0} for x in App.query.all() }
        for dep in Deploy.query.all():
            data[dep.app.id]['count'] += len(json.loads(dep.host_ids))
        data = filter(lambda x: x['count'], data.values())
        return self.jsonify({'host': host, 'res': list(data)})