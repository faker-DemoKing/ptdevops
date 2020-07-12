# -*- coding: utf-8 -*-

from api.extensions import db
from api.libs import Model
from api.libs import human_datetime
from api.libs.ssh import SSH

class Host(Model):
    __tablename__ = 'hosts'

    name = db.Column(db.String(50))
    zone = db.Column(db.String(50))
    hostname = db.Column(db.String(50))
    port = db.Column(db.Integer)
    username = db.Column(db.String(50))
    desc = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.String(20), default=human_datetime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    deleted_at = db.Column(db.String(20), nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def get_ssh(self, pkey=None):
        pkey = pkey or AppSetting.get('private_key')
        return SSH(self.hostname, self.port, self.username, pkey)

    def __str__(self):
        return '<Host %r>' % self.name