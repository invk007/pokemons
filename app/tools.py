import json
import httpx
from httpx import RequestError, HTTPStatusError


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
        response = httpx.get(url)
        response.raise_for_status()
    except RequestError as err:
        raise Exception(f'An error occurred while requesting {err.request.url!r}')
    except HTTPStatusError as err:
        raise Exception(f'Error response {err.response.status_code} while requesting {err.request.url!r}')

    return response.json()


async def async_get(url: str) -> dict:
    """
    Sends a GET request to the specified URL asynchronously and returns the
    response body as a dictionary.

    :param url: the URL to send the GET request to
    :return: a dictionary representing the response body
    :raises Exception: if there is an error while sending the request or parsing
    the response
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
    except RequestError as err:
        raise Exception(f'An error occurred while requesting {err.request.url!r}')
    except HTTPStatusError as err:
        raise Exception(f'Error response {err.response.status_code} while requesting {err.request.url!r}')

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
