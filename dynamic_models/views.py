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
        return context