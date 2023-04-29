import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.tools import async_get, get

logging.basicConfig()
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

API_URL = 'https://pokeapi.co/api/v2/pokemon'
LIMIT = 200


def dump_pokemons_threads() -> list[dict]:
    """
    Retrieves a list of Pokemons from an external API using multiple threads

    :return: list of dicts with pokemons info
    :raises Exception: if there is an error while getting data from the API or
    writing it to file
    """
    try:
        general = get(f'{API_URL}?limit=1')
    except Exception as err:
        _logger.exception(f'Failed to get information from API: {err}')
        raise

    qty = general.get('count', 0)
    offsets = [offset for offset in range(0, qty, LIMIT)]
    pokemons = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                get,
                f'{API_URL}?offset={offset}&limit={LIMIT}',
            )
            for offset in offsets
        ]
        for future in as_completed(futures):
            try:
                data = future.result()
                if 'results' in data:
                    pokemons += data['results']
                else:
                    raise Exception('Unexpected response format')
            except Exception as err:
                _logger.exception(
                    f'Task raised an exception: {err}', exc_info=True
                )

    return pokemons


async def dump_pokemons_async() -> list[dict]:
    """
    Retrieves a list of Pokemons from an external API asynchronously

    :return: list of dicts with pokemons info
    """
    pokemons = []

    try:
        general = await async_get(f'{API_URL}?limit=1')
    except Exception as err:
        _logger.exception(f'Failed to get information from the API: {err}')
        raise

    qty = general.get('count', 0)
    offsets = [offset for offset in range(0, qty, LIMIT)]

    coroutines = [
        async_get(
            f'{API_URL}?offset={offset}&limit={LIMIT}'
        )
        for offset in offsets
    ]

    try:
        results = await asyncio.gather(*coroutines)
        for data in results:
            if 'results' in data:
                pokemons += data['results']
            else:
                raise Exception('Unexpected response format')
    except Exception as err:
        _logger.exception(
            f'Failed to load pokemons information: {err}', exc_info=True
        )

    return pokemons
