# -*- coding:utf-8 -*-

class NotifyCache(object):
    '''
        通知相关的缓存类
    '''
    PREFIX_QUIET = "Notify:quiet"

    @classmethod
    def set_by_time(cls, time):
        cache.set(cls.PREFIX_QUIET, time)
    
    @classmethod
    def get_by_time(cls):
        return cache.get(cls.PREFIX_QUIET)

