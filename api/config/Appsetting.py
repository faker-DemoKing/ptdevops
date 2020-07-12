# -*- coding: utf-8 -*-

from functools import lru_cache
from api.models import Setting

class AppSetting:
    keys = ('public_key', 'private_key', 'mail_service', 'api_key', 'spug_key', 'ldap_service')

    @classmethod
    @lru_cache(maxsize=64)
    def get(cls, key):
        info = Setting.get_by(key=key, to_dict=False, first=True)
        if not info:
            raise KeyError(f'no such key for {key!r}')
        return info.value

    @classmethod
    def get_default(cls, key, default=None):
        info = Setting.get_by(key=key, to_dict=False, first=True)
        if not info:
            return default
        return info.value

    @classmethod
    def set(cls, key, value, desc=None):
        if key in cls.keys:
            Setting.update_or_create(defaults={'value': value, 'desc': desc}, key=key)
        else:
            raise KeyError('invalid key')