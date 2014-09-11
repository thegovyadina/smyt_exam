#-*- coding: UTF-8 -*-
from django.contrib import admin
from django.db import models
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


def read_yaml():
    models_list = []
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

    return models_list


def read_xml():
    models_list = []
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
    return models_list


def get_models_configs():

    ext = MODELS_CONFIG_FILE.split('.')[-1]

    if ext in ('yml', 'yaml'):
        result = read_yaml()

    elif ext == 'xml':
        result = read_xml()

    else:
        raise DynamicModelsConfigError('Unsupported file type: %s' % MODELS_CONFIG_FILE)

    return result
