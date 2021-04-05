from django.apps import AppConfig


class ExplorerConfig(AppConfig):
    name = 'explorer'

    API_BASE_URL = 'https://swapi.dev/api/'
    COLLECTIONS_PATH = 'explorer/data'


