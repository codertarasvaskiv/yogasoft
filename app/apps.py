from django.apps import AppConfig as AppConfig2


class AppConfig(AppConfig2):
    name = 'app'

    def __init__(self):
        pass
