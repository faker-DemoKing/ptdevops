# -*- coding:utf-8 -*-

import json

from api.extensions import db
from api.libs.database import Model
from api.libs.utils import human_datetime

class TaskHistoryStatus(Model):
    __tablename__ = 'task_histories_status'
    
    name = db.Column(db.String(50))

class TaskHistory(Model):
    __tablename__ = 'task_histories'

    task_id = db.Column(db.Integer)
    status = db.Column(db.Integer, db.ForeignKey('task_histories_status.id'))
    run_time = db.Column(db.String(20))
    output = db.Column(db.Text)

class TaskTrigger(Model):
    __tablename__ = 'task_triggers'
    
    name = db.Column(db.String(50))

    def __str__(self):
        return '<TaskTrigger %r>' % self.name

class Task(Model):
    __tablename__ = 'tasks'

    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    command = db.Column(db.Text)
    targets = db.Column(db.Text)
    trigger = db.Column(db.Integer, db.ForeignKey('task_triggers.id'))
    trigger_args = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    desc = db.Column(db.String(255), nullable=True)
    latest = db.Column(db.Integer, db.ForeignKey('task_histories.id'),nullable=True)
    rst_notify = db.Column(db.String(255), nullable=True)

    create_at = db.Column(db.String(20), default=human_datetime)
    create_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_at = db.Column(db.String(20))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['targets'] = json.loads(self.targets)
        tmp['latest_status'] = self.latest.status if self.latest else None
        tmp['latest_run_time'] = self.latest.run_time if self.latest else None
        tmp['latest_status_alias'] = self.get_latest_status_display() if self.latest else None
        tmp['rst_notify'] = json.loads(self.rst_notify) if self.rst_notify else {'model': '0'}
        if self.trigger == 'cron':
            tmp['trigger_args'] = json.loads(self.trigger_args)
        return tmp
    
    def __str__(self):
        return '<Task %r>' % self.name
