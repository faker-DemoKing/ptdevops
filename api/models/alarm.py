# -*- coding:utf-8 -*-
import json

from api.extensions import db
from api.libs import Model
from api.libs import human_datetime

class AlarmStatus(Model):
    """
        alarm status表
        状态就 1 和 0 
        0代表报警发生
        1代表故障恢复
    """
    __tablename__ = 'alarms_status'

    name = db.Column(db.String(50))

    def __str__(self):
        return ('<AlarmStatus %r>') % self.name

class Alarm(Model):
    """
        alarm表
    """
    __tablename__ = 'alarms'

    MODES = (
        ('1', '微信'),
        ('2', '短信'),
        ('3', '钉钉'),
        ('4', '邮件'),
        ('5', 'telgram'),
    )

    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    notify_mode = db.Column(db.String(255))
    notify_grp = db.Column(db.String(255))
    status = db.Column(db.Integer, db.ForeignKey('alarms_status.id'))
    duration = db.Column(db.String(50))
    created_at = db.Column(db.String(20), default=human_datetime)
    
    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['notify_mode'] = ','.join(dict(self.MODES)[x] for x in json.loads(self.notify_mode))
        tmp['notify_grp'] = json.loads(self.notify_grp)
        tmp['status_alias'] = self.get_status_display() # 这里有问题
        return tmp

    def __str__(self):
        return '<Alarm %r>' % self.name

class AlarmGroup(Model):
    """
        报警组
    """
    __tablename__ = 'alarm_groups'

    name = db.Column(db.String(50))
    desc = db.Column(db.String(255), nullable=True)
    contacts = db.Column(db.Text, nullable=True)
    create_at = db.Column(db.String(20), default=human_datetime)
    create_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['contacts'] = json.loads(self.contacts)
        return tmp
    
    def __str__(self, *args, **kwargs):
        return '<AlarmGroup %r>' % self.name

class AlarmContact(Model):
    """
        报警联系人表
    """
    __tablename__ = 'alarm_contacts'

    name = db.Column(db.String(50))
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    ding = db.Column(db.String(255), nullable=True)
    wx_token = db.Column(db.String(255), nullable=True)
    qy_wx = db.Column(db.String(255), nullable=True)
    create_at = db.Column(db.String(20), default=human_datetime)
    create_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __str__(self, *args, **kwargs):
        return '<AlarmGroup %r>' % self.name