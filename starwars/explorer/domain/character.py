from math import ceil
import os
from urllib.parse import urljoin

from dateutil import parser
from django.apps import apps
from petl import fromdicts, addfield, cutout, convert
import petl
import requests

from explorer.domain.homeworld import get_homeworld_names
from explorer.utils import run_parallel

HEADERS = ('name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color',
           'birth_year', 'gender', 'homeworld', 'edited')


def get_characters(uri: str) -> dict:
    """
    Returns data for characters for given URI endpoint.

    :param uri: URI of the API endpoint for listing characters.
    :return: Return dictionary with characters data and meta data.
    """
    response = requests.get(uri)
    characters = response.json()
    return characters


# We don't have to declare new classes or create new instances
def process(filepath):
    while True:
        characters = (yield)
        planet_mapping = get_homeworld_names([item['homeworld'] for item in characters['results']])
        table = fromdicts(characters['results'], header=HEADERS)
        table = addfield(table, 'date', lambda row: parser.isoparse(row['edited']).strftime('%Y-%m-%d'))
        table = cutout(table, 'edited')
        table = convert(table, 'homeworld', lambda uri: planet_mapping[uri])

        if os.path.exists(filepath):
            petl.appendcsv(table, filepath)
        else:
            petl.tocsv(table, filepath, write_header=True)


def get_pipeline(collection_filepath):
    p = process(collection_filepath)
    next(p)
    return p


def download_collection(collection_filepath: str):
    app_config = apps.get_app_config('explorer')
    characters = get_characters(urljoin(app_config.API_BASE_URL, 'people/'))
    pipeline = get_pipeline(collection_filepath)
    pipeline.send(characters)
    pages = [f'{urljoin(app_config.API_BASE_URL, "people/")}?page={number}'
             for number in range(2, ceil(characters['count'] / 10) + 1)]

    for characters in run_parallel(pages, get_characters):
        pipeline.send(characters)
