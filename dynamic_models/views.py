# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models.loading import get_app, get_models, get_model
from django.views.generic.base import TemplateView, View
from mixins import JsonResponseMixin


def get_model_data(model):
    values = [m for m in model.objects.all().order_by('id').values_list()]
    fields = [(getattr(f, "verbose_name"), f.name, f.get_internal_type().lower()) for f in model._meta.fields]
    return fields, values


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        models = []

        for model in get_models(get_app('dynamic_models')):
            models.append([model.__name__, model._meta.verbose_name])

        context['models'] = models

        return context


class ModelView(View, JsonResponseMixin):

    def get(self, request):
        context = {}
        model = request.GET.get('model')
        if model is not None:
            model = get_model('dynamic_models', model)

            model_fields, model_values = get_model_data(model)

            context = {
                'fields': model_fields,
                'values': model_values,
            }
        return JsonResponseMixin.render_to_reponse(context)

    def post(self, request):
        context = {}
        id = request.POST.get('id')

        if id is not None:
            model = get_model('dynamic_models', request.POST.get('model')).objects.get(id=int(id))
        else:
            model = get_model('dynamic_models', request.POST.get('model'))()

        for field in model._meta.fields:
            if field.name not in request.POST:
                continue
            value = request.POST[field.name]
            if field.get_internal_type() == 'DateField':
                value = datetime.strptime(value, '%d.%m.%Y')

            setattr(model, field.name, value)
        model.save()

        return JsonResponseMixin.render_to_reponse(context)