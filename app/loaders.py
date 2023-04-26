import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from app import constants
from app.tools import async_get, get, save_to_file

logging.basicConfig()
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


def dump_pokemons_threads():
    """
    Retrieves a list of Pokemons from an external API using multiple threads,
    and saves it to a file.

    :return: None
    :raises Exception: if there is an error while getting data from the API or
    writing it to file
    """
    try:
        general = get(f'{constants.API_URL}?limit=1')
    except Exception as err:
        _logger.exception(f'Failed to get information from API: {err}')
        return

    qty = general.get('count', 0)
    offsets = [offset for offset in range(0, qty, constants.LIMIT)]
    pokemons = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                get,
                f'{constants.API_URL}?offset={offset}&limit={constants.LIMIT}',
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

    save_to_file('pokemons_threads.json', pokemons)


async def dump_pokemons_async():
    """
    Retrieves a list of Pokemons from an external API asynchronously, and saves
    it to a file.

    :return:
    """
    pokemons = []

    try:
        general = await async_get(f'{constants.API_URL}?limit=1')
    except Exception as err:
        _logger.exception(f'Failed to get information from the API: {err}')
        return

    qty = general.get('count', 0)
    offsets = [offset for offset in range(0, qty, constants.LIMIT)]

    coroutines = [
        async_get(
            f'{constants.API_URL}?offset={offset}&limit={constants.LIMIT}'
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

    save_to_file('pokemons_async.json', pokemons)


def dump_pokemons_seq():
    """
    Retrieves a list of Pokemons from an external API sequentially, and saves it
    to a file.
    :return:
    """
    pokemons = []
    next_ = f'{constants.API_URL}?limit={constants.LIMIT}'

    while next_:
        result = get(next_)
        pokemons += result.get('results', [])
        next_ = result.get('next')

    save_to_file('pokemons_seq.json', pokemons)
