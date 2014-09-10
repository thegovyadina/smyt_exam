#-*- coding: UTF-8 -*-
from django.db.models.fields import CharField, DateField, IntegerField
from lxml import etree
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from settings import MODELS_CONFIG_FILE


class DynamicModelsConfigError(Exception):
    pass


def set_field_type(field_type, **kwargs):

    if field_type == 'char':
        return CharField(max_length=100, **kwargs)

    elif field_type == 'int':
        return IntegerField(**kwargs)

    elif field_type == 'date':
        return DateField(**kwargs)

    raise DynamicModelsConfigError("Unsupported field type '%s' in %s" % (field_type, MODELS_CONFIG_FILE))


def get_models_configs():

    models_list = []

    if MODELS_CONFIG_FILE.endswith('.yml'):
        models = load(file(MODELS_CONFIG_FILE), Loader=Loader)

        for model_name, model in models.iteritems():
            fields = {}

            for field in model['fields']:

                kwargs = {
                    'verbose_name': field['title'],
                    'blank': True,
                    'null': True,
                }

                fields.update({
                    field['id']: set_field_type(field['type'], **kwargs)
                })

            models_list.append({
                'name': model_name,
                'fields': fields,
                'verbose_name': model['title'],
            })

    elif MODELS_CONFIG_FILE.endswith('.xml'):
        tree = etree.parse(MODELS_CONFIG_FILE)
        models = tree.xpath('//models/model')

        for model in models:
            fields_dict = {}

            for field in model.getchildren():
                kwargs = {
                    'verbose_name': field.attrib['title'],
                    'blank': True,
                    'null': True,
                }

                fields_dict.update({
                    field.attrib['id']: set_field_type(field.attrib['type'], **kwargs)
                })

            models_list.append({
                'name': model.attrib['name'],
                'fields': fields_dict,
                'verbose_name': model.attrib['title'],
            })

    else:
        raise DynamicModelsConfigError('Unsupported file type: %s' % MODELS_CONFIG_FILE)

    return models_list