import json
import typing as t

import requests
from requests import HTTPError


def get(url: str) -> t.Dict:
    """
    Executes GET request to the API

    :param url:
    :return:
    """
    try:
        response = requests.get(url)
    except HTTPError as err:
        raise Exception(f'Request to API failed with error: {err}')
    except Exception:
        raise Exception('Unexpected error while getting data from API')

    return response.json()


def save_to_file(filename: str, pokemons: list[dict]):
    with open(filename, 'w') as f:
        json.dump(pokemons, f)
