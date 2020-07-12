# -*- coding: utf-8 -*-

from flask import request
from api.resource import APIView
from api.models import Notify

class NotifyView(APIView):
    """
        notify视图
    """
    url_prefix = "/notify"

    def get(self):
        notifies = Notify.get_by(unread=True)
        return self.jsonify(notifies)
    
    def patch(self):
        for notify in Notify.get_by_in_id(ids=request.values['ids'],to_dict=False):
            notify.update(unread=False)
        
        return self.jsonify(error='')