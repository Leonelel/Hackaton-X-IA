# chatbox/apps.py
from django.apps import AppConfig

class ChatboxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbox'

    def ready(self):
        # Import and connect signals
        from . import signals