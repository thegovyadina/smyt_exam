import json
import datetime
from django.http import HttpResponse


def default(obj):
    if isinstance(obj, datetime.date):
        return obj.strftime("%d.%m.%Y")

class JsonResponseMixin(object):

    @staticmethod
    def render_to_reponse(context):
        try:
            result = json.dumps(context, default=default)
        except (AttributeError, TypeError):
            result = json.dumps({'error': 1, 'error_msg': 'JSON serialization error'})
        return HttpResponse(result, content_type='application/json')