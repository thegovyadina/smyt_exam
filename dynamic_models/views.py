from django.db.models.loading import get_app, get_models, get_model
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        models = []

        for model in get_models(get_app('dynamic_models')):
            models.append([model.__name__, model._meta.verbose_name])

        context['models'] = models

        first_model = get_model('dynamic_models', models[0][0])
        first_model_data = [m for m in first_model.objects.all().values_list()]
        first_model_fields = [(f._verbose_name, f.get_internal_type().lower()) for f in first_model._meta.fields]
        context['first_model'] = first_model_data
        context['first_model_fields'] = first_model_fields

        return context