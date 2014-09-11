from django.db import models
from django.contrib import admin
from config import get_models_configs


class Meta:
    pass

models_list = []
for config_model in get_models_configs():
    setattr(Meta, 'verbose_name', config_model['verbose_name'])
    setattr(Meta, 'verbose_name_plural', config_model['verbose_name'])
    model = type(config_model['name'], (models.Model,), {'Meta': Meta, '__module__': __name__})
    for field_name, field in config_model['fields'].iteritems():
        model.add_to_class(field_name, field)
    models_list.append(model)
    try:
        admin.site.register(model)
    except:
        pass

