# -*- coding: utf-8 -*-

from api.extensions import db
from api.libs import Model

class Setting(Model):
    __tablename__ = 'settings'

    key = db.Column(db.String(50), unique=True)
    value =  db.Column(db.Text)
    desc = db.Column(db.String(255), nullable=True)

    def __str_(self):
        return '<Setting %r>' % self.key
