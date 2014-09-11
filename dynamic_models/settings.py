import os

from django.conf import settings


APP_DIR = os.path.abspath(os.path.dirname(__file__))

MODELS_CONFIG_FILE = getattr(settings, 'MODELS_CONFIG_FILE', os.path.join(APP_DIR, "model_configs/models.json"))