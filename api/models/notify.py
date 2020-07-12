# -*- coding:utf-8 -*-

from api.extensions import db
from api.libs import Model, human_datetime
from api.libs.cache.notify import NotifyCache


class NotifyType(Model):
    __tablename__ = 'notify_type'

    name = db.Column(db.String(20),nullable=True)

    def __str__(self):
        return '<NotifyType %r>' % self.name

class NotifySource(Model):
    __tablename__ = 'notify_source'

    name = db.Column(db.String(10),nullable=True)
    desc = db.Column(db.String(20),nullable=True)

    def __str__(self):
        return '<NotifySource %r>' % self.name

class Notify(Model):
    """"""
    __tablename__ = 'notify'

    title = db.Column(db.String(255))
    source = db.Column(db.Integer, db.ForeignKey('notify_source.id'), nullable=True)
    type = db.Column(db.Integer, db.ForeignKey('notify_type.id'), nullable=True)
    content = db.Column(db.String(255), nullable=True)
    unread = db.Column(db.Boolean, default=True)
    link = db.Column(db.Boolean, nullable=True)

    created_at = db.Column(db.String(20), default=human_datetime)

    @classmethod
    def make_notify(cls, source, type, title, content=None, with_quiet=True):
        if not with_quiet or time.time() - NotifyCache.get_by_time() > 3600:
            NotifyCache.set_by_time(time.time())
            self.create(source=source, title=title, type=type, content=content)

    def __str__(self):
        return '<Notify %r>' % self.title