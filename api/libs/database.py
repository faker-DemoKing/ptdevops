# -*- coding:utf-8 -*-

import datetime
import six

from api.extensions import db
from api.libs.exception import CommitException


class ModelMixin(object):
    def to_dict(self, excludes: tuple = None, selects: tuple = None) -> dict:
        if selects:
            return {f: getattr(self, f) for f in selects}
        elif excludes:
            return {f.attname: getattr(self, f.attname) for f in self._meta.fields if f.attname not in excludes}
        else:
            return {f.attname: getattr(self, f.attname) for f in self._meta.fields}
    # def to_dict(self):
    #     res = dict()
    #     for k in getattr(self, "__table__").columns:
    #         if not isinstance(getattr(self, k.name), datetime.datetime):
    #             res[k.name] = getattr(self, k.name)
    #         else:
    #             res[k.name] = getattr(self, k.name).strftime('%Y-%m-%d %H:%M:%S')
    #     return res
        
    @classmethod
    def get_columns(cls):
        return {k.name: 1 for k in getattr(cls, "__mapper__").c.values()}

class CRUDMixin(ModelMixin):

    def __init__(self, **kwargs):
        super(CRUDMixin, self).__init__(**kwargs)

    @classmethod
    def create(cls, flush=False, defaults=None, **kwargs):
        if defaults:
            for key, value in defaults.items():
                kwargs[key] = value
        return cls(**kwargs).save(flush=flush)
    
    def update(self, flush=False, **kwargs):
        kwargs.pop("id", None) # id不需要更新，所以刨除id
        for attr, value in six.iteritems(kwargs):
            if value is not None:
                setattr(self, attr, value)
        if flush:
            return self.save(flush=flush)
        return self.save()
    
    def save(self, commit=True, flush=False):
        db.session.add(self)
        try:
            if flush:
                db.session.flush()
            elif commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CommitException(str(e))

        return self

    @classmethod
    def update_or_create(cls, defaults, *args, **kwargs):
        key = cls.get_by(first=True, to_dict=False, **kwargs)
        if key:
            key.update(defaults)
        else:
            cls.create(defaults=defaults, **kwargs)

    @classmethod
    def get_by_in_id(cls, first=False, to_dict=True, ids=None):
        result = [i.to_dict() if to_dict else i for i in cls.query.filter(cls.id.in_(ids)) ]

        return result[0] if first and result else (None if first else result)

    @classmethod
    def get_by(cls, first=False, to_dict=True, fl=None, exclude=None, deleted=None, use_master=False, **kwargs):
        db_session = db.session if not use_master else db.session().using_bind("master")
        fl = fl.strip().split(",") if fl and isinstance(fl, six.string_types) else (fl or [])
        exclude = exclude.strip().split(",") if exclude and isinstance(exclude, six.string_types) else (exclude or [])

        keys = cls.get_columns()
        fl = [k for k in fl if k in keys]
        fl = [k for k in keys if k not in exclude and not k.isupper()] if exclude else fl
        fl = list(filter(lambda x: "." not in x, fl))

        if hasattr(cls, "deleted_at") and deleted is not None:
            kwargs["deleted_at"] = deleted

        if fl:
            query = db_session.query(*[getattr(cls, k) for k in fl])
            query = query.filter_by(**kwargs)
            result = [{k: getattr(i, k) for k in fl} for i in query]
        else:
            result = [i.to_dict() if to_dict else i for i in getattr(cls, 'query').filter_by(**kwargs)]

        return result[0] if first and result else (None if first else result)

class SurrogatePK(object):
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Model(db.Model, CRUDMixin, SurrogatePK):
    __abstract__ = True

class CRUDModel(db.Model, CRUDMixin, SurrogatePK):
    __abstract__ = True
