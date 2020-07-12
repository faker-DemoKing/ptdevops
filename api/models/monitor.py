# -*- coding:utf-8 -*-

from api.extensions import db
from api.libs.database import Model
from api.libs.utils import human_datetime
import json

class DetectionType(Model):
    __tablename__ = 'detection_types'

    name = db.Column(db.String(50))

class DetectionStatus(Model):
    __tablename__ = 'detection_status'

    name = db.Column(db.String(50))

class Detection(Model):
    __tablename__ = 'detections'

    name = db.Column(db.String(50))
    type = db.Column(db.Integer, db.ForeignKey('detection_types.id'))
    addr = db.Column(db.String(255))
    extra = db.Column(db.Text, nullable=True)
    desc = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    rate = db.Column(db.Integer, default=5)
    threshold = db.Column(db.Integer, default=3)
    quiet = db.Column(db.Integer, default=24 * 60)
    fault_times = db.Column(db.SmallInteger, default=0)
    notify_mode = db.Column(db.String(255))
    notify_grp = db.Column(db.String(255))
    latest_status = db.Column(db.Integer, db.ForeignKey('detection_status.id'), nullable=True)
    latest_run_time = db.Column(db.String(20), nullable=True)
    latest_fault_time = db.Column(db.Integer, nullable=True)
    latest_notify_time = db.Column(db.Integer, default=0)

    create_at = db.Column(db.String(20), default=human_datetime)
    create_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_at = db.Column(db.String(20))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['type_alias'] = self.get_type_display()
        tmp['latest_status_alias'] = self.get_latest_status_display()
        tmp['notify_mode'] = json.loads(self.notify_mode)
        tmp['notify_grp'] = json.loads(self.notify_grp)
        return tmp
    
    def __str__(self):
        return '<Detection %r>' % slef.name 