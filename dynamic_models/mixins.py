import json
from django.http import HttpResponse


class JsonResponseMixin(object):

    @staticmethod
    def render_to_reponse(context):
        try:
            result = json.dumps(context)
        except (AttributeError, TypeError):
            result = json.dumps({'error': 1, 'error_msg': 'JSON serialization error'})
        return HttpResponse(result, content_type='application/json')