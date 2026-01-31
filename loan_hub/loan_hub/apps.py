from django.apps import AppConfig
from threading import Thread

class LoanHubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loan_hub'

    def ready(self):
        pass   # keep empty for now

