import datetime
import string
import json
from django.db.models.loading import get_app, get_models
from django.test import TestCase
from random import randint, randrange, choice


class DynamicModelsViewsTestCase(TestCase):

    def test_getmodel(self):
        models = get_models(get_app('dynamic_models'))

        for model in models:
            model_instanse = model()
            for field in model._meta.fields:
                if field.get_internal_type() == "IntegerField":
                    setattr(model_instanse, field.name, randrange(10000))
                elif field.get_internal_type() == "DateField":
                    year = randint(1990, 2014)
                    month = randint(1, 12)
                    day = randint(1, 28)
                    setattr(model_instanse, field.name, datetime.datetime(year, month, day))
                if field.get_internal_type() == "CharField":
                    setattr(model_instanse, field.name, ''.join(choice(string.lowercase) for i in range(200)))

        for model in models:
            url = '/model/?model=%s' % model.__name__
            resp = self.client.get(url)
            json_response = json.loads(resp.content)
            self.assertEqual(resp.status_code, 200)
            self.assertTrue('fields' in json_response)
            self.assertTrue('values' in json_response)

