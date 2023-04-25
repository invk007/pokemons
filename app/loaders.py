import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from app import constants
from app.tools import get, save_to_file, timer

logging.basicConfig()
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


@timer
def dump_pokemons_threads():
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
                    raise Exception('Unexpected format error')
            except Exception as err:
                _logger.exception(f'Task raised an exception: {err}')

    save_to_file('pokemons_threads.json', pokemons)


@timer
def dump_pokemons_seq():
    pokemons = []
    next_ = f'{constants.API_URL}?limit={constants.LIMIT}'

    while next_:
        result = get(next_)
        pokemons += result.get('results', [])
        next_ = result.get('next')

    save_to_file('pokemons_seq.json', pokemons)
