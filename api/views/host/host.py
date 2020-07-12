# -*- coding:utf-8 -*-

from flask import request, g
from paramiko.ssh_exception import AuthenticationException
from sqlalchemy import and_

from api.libs.utils import AttrDict
from api.extensions import db
from api.config.Appsetting import AppSetting
from api.resource import APIView
from api.libs.ssh import SSH
from api.models import Host, Deploy, Role, Task

class HostView(APIView):
    '''
        主机视图
    '''
    # url_prefix = '/hosts'

    def get(self):
        '''
            获取所有的zones和主机
        '''
        host_id = request.values.get('id')
        if host_id:
            if not g.user.has_host_perm(host_id):
                return self.jsonify(error='无权访问该主机')
        hosts = Host.query.filter(Host.deleted_at.is_(None)).all()
        zones = [i.zone for i in hosts if i.zone ]
        perms = [x.id for x in hosts] if g.user.is_supper else g.user.host_perms
        return self.jsonify({'zones': zones, 'hosts': [x.to_dict() for x in hosts], 'perms': perms})
    
    def post(self):
        '''
            添加主机
        '''
        id = request.values.get('id', None)
        zone = request.values.get('zone', None)
        name = request.values.get('name',None)
        username = request.values.get('username', None)
        password = request.values.pop('password', None)
        hostname = request.values.get('hostname', None)
        port = request.values.get('port', None)
        if valid_ssh(hostname, port, username, password) is False:
            return self.jsonify('auth fail')
        if id:
            Host.get_by(id=id, to_dict=False).update(request.values)
        elif Host.query.filter(db.exists().where(and_(Host.name==name,Host.deleted_by.is_(None)))).scalar():
            return self.jsonify(error='已存在的主机名称【%s】' % name)
        else:
            request.values['created_by'] = g.user.id
            host = Host.create(**request.values)
            if g.user.role:
                g.user.role.add_host_perm(host.id)
        return self.jsonify(error='')
    
    def delete(self):
        ''''
            删除主机
        '''
        data = AttrDict(id=request.values['id'])
        deploy = Deploy.query.filter(Deploy.host_ids.op('regexp')(fr"(\[.*\,|\[){data.id}(\]|\,.*\])")).first()
        if deploy:
            return self.jsonify(error=f'应用【{deploy.app.name}】在【{deploy.env.name}】的发布配置关联了该主机，请解除关联后再尝试删除该主机')
        task = Task.query.filter(Task.targets.op('regexp')(fr"(\[.*\,|\[){data.id}(\]|\,.*\])")).first()
        if task:
            return self.jsonify(error=f'任务计划中的任务【{task.name}】关联了该主机，请解除关联后再尝试删除该主机')
        # return 

def valid_ssh(hostname, port, username, password):
    try:
        private_key = AppSetting.get('private_key')
        public_key = AppSetting.get('public_key')
    except KeyError:
        private_key, public_key = SSH.generate_key()
        AppSetting.set('private_key', private_key, 'ssh private key')
        AppSetting.set('public_key', public_key, 'ssh public key')
    if password:
        cli = SSH(hostname, port, username, password=password)
        code, out = cli.exec_command('mkdir -p -m 700 ~/.ssh && \
                echo %r >> ~/.ssh/authorized_keys && \
                chmod 600 ~/.ssh/authorized_keys' % public_key)
        if code != 0:
            raise Exception(f'add public key error: {out!r}')
    else:
        cli = SSH(hostname, port, username, private_key)
    
    try:
        cli.ping()
    except AuthenticationException:
        return False
    return True