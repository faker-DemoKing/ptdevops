# -*- coding:utf-8 -*-

from api.extensions import db
from api.libs.database import Model
from api.libs.utils import human_datetime


class Environment(Model):
    __tablename__ = 'environments'

    name = db.Column(db.String(50))
    key = db.Column(db.String(50))
    desc = db.Column(db.String(255), nullable=True)
    create_at = db.Column(db.String(20), default=human_datetime)
    create_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __str__(self):
        return '<Environment %r>' % self.name
    
class Service(Model):
    __tablename__ = 'services'

    name = db.Column(db.String(50))
    key = db.Column(db.String(50))
    desc = db.Column(db.String(255), nullable=True)
    create_at = db.Column(db.String(20), default=human_datetime)
    create_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __str__(self):
        return '<Service %r>' % self.name
    
class ConfigType(Model):
    __tablename__ = 'config_types'

    name = db.Column(db.String(50))

    def __str__(self):
        return '<ConfigType %r>' % self.name

class ConfigHistoryAction(Model):
    __tablename__ = 'config_history_actions'

    name = db.Column(db.String(50))

    def __str__(self):
        return 'ConfigHistoryAction %r' % self.name

class Config(Model):
    __tablename__ = 'configs'

    type = db.Column(db.Integer, db.ForeignKey('config_types.id'))
    o_id = db.Column(db.Integer)
    key = db.Column(db.String(50))
    env =  db.Column(db.Integer, db.ForeignKey('environments.id'))
    value = db.Column(db.Text, nullable=True)
    desc = db.Column(db.String(255), nullable=True)
    is_public = db.Column(db.Boolean)
    updated_at = db.Column(db.String(20))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __str__(self):
        return '<Config %r>' % self.key

class ConfigHistory(Model):
    __tablename__ = 'config_histories'

    type = db.Column(db.String(5))
    o_id = db.Column(db.Integer)
    key = db.Column(db.String(50))
    env_id = db.Column(db.Integer)
    value = db.Column(db.Text, nullable=True)
    desc = db.Column(db.String(255), nullable=True)
    is_public = db.Column(db.Boolean)
    old_value = db.Column(db.Text, nullable=True)
    action = db.Column(db.Integer, db.ForeignKey('config_history_actions.id'))
    updated_at = db.Column(db.String(20))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __str__(self):
        return '<ConfigHistory %r>' % self.key