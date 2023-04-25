import json
import time
import typing as t
from functools import wraps

import requests
from requests import HTTPError


def timer(func: t.Callable) -> t.Callable:
    """
    Measure function running time.

    :param func:
    :return:
    """

    @wraps(func)
    def inner(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Function run time = {end - start}')
        return result

    return inner


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
    except Exception as err:
        raise Exception('Unexpected error while getting data from API')

    return response.json()


def save_to_file(filename: str, pokemons: list[dict]):
    with open(filename, 'w') as f:
        json.dump(pokemons, f)
