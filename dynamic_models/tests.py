# -*- coding: utf-8 -*-
import datetime
import string
import json
from django.db.models.loading import get_app, get_models
from django.test import TestCase
from random import randint, randrange, choice


def rnd_date():
    year = randint(1990, 2014)
    month = randint(1, 12)
    day = randint(1, 28)
    return datetime.datetime(year, month, day)


def rnd_str():
    return ''.join(choice(string.lowercase) for i in range(100))


class DynamicModelsViewsTestCase(TestCase):

    def test_model_requests(self):
        """
        Создаем запись POST-ом, потом читаем GET-ом и убеждаемся, что получили то, что сохранили
        """

        models = get_models(get_app('dynamic_models'))
        post_data = {}

        for model in models:
            post_data[model.__name__] = {}
            for field in model._meta.fields:
                if field.get_internal_type() == "IntegerField":
                    post_data[model.__name__][field.name] = randrange(10000)
                elif field.get_internal_type() == "DateField":
                    post_data[model.__name__][field.name] = rnd_date().strftime("%d.%m.%Y")
                if field.get_internal_type() == "CharField":
                    post_data[model.__name__][field.name] = rnd_str()

        # POST
        for model_name in post_data:
            query = {'model': model_name}
            query.update(post_data[model_name])
            resp = self.client.post('/model/', query)
            self.assertEqual(resp.status_code, 200)

        # GET
        for model_name in post_data:
            url = '/model/?model=%s' % model_name
            resp = self.client.get(url)
            json_response = json.loads(resp.content)
            self.assertEqual(resp.status_code, 200)
            for value in post_data[model_name].values():
                self.assertIn(value, json_response['values'][0])
