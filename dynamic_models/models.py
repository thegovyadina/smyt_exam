# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from config import get_models_configs


class Meta:
    pass

for config_model in get_models_configs():

    for name in ('verbose_name', 'verbose_name_plural'):
        setattr(Meta, name, config_model['verbose_name'])

    attrs = {
        'Meta': Meta,
        '__module__': __name__,
    }

    # Если у модели есть поле "name", используем его для наименования записей в админке
    if 'name' in config_model['fields']:
        attrs.update({'__unicode__': lambda self: self.name})

    model = type(
        str(config_model['name']),
        (models.Model,),
        attrs
    )

    for field_name, field in config_model['fields'].iteritems():
        model.add_to_class(field_name, field)

    try:
        admin.site.register(model)
    except admin.site.AlreadyRegistered:
        pass

