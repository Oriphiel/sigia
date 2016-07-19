'''
Created on 29/12/2014

@author: Dario
'''

from django.http import QueryDict
from sigia.utils import case_insensitive_key
import pytz
from django.utils import timezone

class HttpPostTunnelingMiddleware(object):
    def process_request(self, request):
        http_method = None
        if request.META.has_key('HTTP_X_METHODOVERRIDE'):
            http_method = request.META['HTTP_X_METHODOVERRIDE']
        else:
            http_method = case_insensitive_key(request.POST, 'ACTION')
            if len(http_method) > 0 :
                http_method = http_method[0]
        if http_method:            
            if http_method.lower() == 'put':
                request.META['REQUEST_METHOD'] = 'PUT'
                request.PUT = QueryDict(request.body)
            if http_method.lower() == 'delete':
                request.META['REQUEST_METHOD'] = 'DELETE'
                request.DELETE = QueryDict(request.body)
        return None
    
class TimezoneMiddleware(object):
    def process_request(self, request):
        timezone.activate(pytz.timezone("America/Guayaquil"))