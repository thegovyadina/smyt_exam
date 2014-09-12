from django.db.models.loading import get_app, get_models, get_model
from django.views.generic.base import TemplateView, View
from mixins import JsonResponseMixin


def get_model_data(model):
    values = [m for m in model.objects.all().values_list()]
    fields = [(f._verbose_name, f.get_internal_type().lower()) for f in model._meta.fields]
    return fields, values


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        models = []

        for model in get_models(get_app('dynamic_models')):
            models.append([model.__name__, model._meta.verbose_name])

        context['models'] = models

        first_model = get_model('dynamic_models', models[0][0])
        first_model_fields, first_model_values = get_model_data(first_model)
        context['first_model'] = first_model_values
        context['first_model_fields'] = first_model_fields

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