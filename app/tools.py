import json

import requests
from requests import HTTPError


def get(url: str) -> dict:
    """
    Sends a GET request to the specified URL and returns the response body as a
    dictionary.

    :param url: the URL to send the GET request to
    :return: a dictionary representing the response body
    :raises Exception: if there is an error while sending the request or parsing
    the response
    """
    try:
        response = requests.get(url)
    except HTTPError as err:
        raise Exception(f'Request to API failed with error: {err}')
    except Exception:
        raise Exception('Unexpected error while getting data from API')

    return response.json()


def save_to_file(filename: str, pokemons: list[dict]):
    """
    Saves a list of dictionaries representing Pokemons to a file in JSON format.

    :param filename: the path to the output file
    :param pokemons: a list of dictionaries representing the Pokemons to be saved
    :return: None
    :raises IOError: if there is an error while writing to the file
    """
    with open(filename, 'w') as f:
        json.dump(pokemons, f)
