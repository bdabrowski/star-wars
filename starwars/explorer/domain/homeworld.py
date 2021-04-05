from functools import lru_cache
import logging
from typing import Tuple, Dict, List

import requests

from explorer.utils import run_parallel

logger = logging.getLogger('django')


@lru_cache(maxsize=1024)
def resolve_homeworld(uri: str) -> Tuple[str, str]:
    """
    Map URI of planet to it's name.

    :param uri: URI of API endpoint for particular planet.
    :return: The 2-element tuple where first item is uri and second item is planet's name.
    """
    response = requests.get(uri)
    data = response.json()
    return uri, data['name']


def get_homeworld_names(uris: List[str]) -> Dict:
    """
    Get mapping of homeworld name from URIs.

    :param uris: List of URIs of API endpoints for particular planets.
    :return: Dictionary of mapping URI into planet's name.
    """
    return dict([mapping for mapping in run_parallel(uris, resolve_homeworld, n=10)])
