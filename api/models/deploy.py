# -*- coding:utf-8 -*-

from api.extensions import db
from api.libs.database import Model
from api.libs.utils import human_datetime

class DeployRequestStatus(Model):
    '''
        deploy_request_status表
    '''
    __tablename__ = 'deploy_request_status'

    name = db.Column(db.String(50))

class DeployRequestType(Model):
    '''
     deploy_request_types表
    '''
    __tablename__ = 'deploy_request_types'

    name = db.Column(db.String(50))

class DeployRequest(Model):
    '''
        deploy_requests表
    '''
    __tablename__ = 'deploy_requests'

    deploy = db.Column(db.Integer, db.ForeignKey('deploys.id'))
    name = db.Column(db.String(50))
    type = db.Column(db.Integer, db.ForeignKey('deploy_request_types.id'), default=1)
    extra = db.Column(db.Text)
    host_ids = db.Column(db.Text)
    desc = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Integer, db.ForeignKey('deploy_request_status.id'))
    reason = db.Column(db.String(255), nullable=True)
    version = db.Column(db.String(50), nullable=True)

    create_at = db.Column(db.String(20), default=human_datetime)
    create_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approve_at = db.Column(db.String(20), nullable=True)
    approve_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __str__(self):
        return '<DeployRequest name=%r>' % self.name

