import httpx
import pytest
from httpx import Response
from pytest_mock import MockFixture

from app.tools import get, async_get

TEST_URL = 'https://example.com'


def test__get__request_successful(mocker: MockFixture):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {'key': 'value'}
    mocker.patch('httpx.get', return_value=mock_response)

    result = get(TEST_URL)

    assert result == {'key': 'value'}


def test__get__request_fails_with_request_error(mocker: MockFixture):
    mock_request = mocker.Mock()
    mock_request.request.url = TEST_URL
    mocker.patch(
        'httpx.get',
        side_effect=httpx.RequestError('Request error', request=mock_request),
    )

    with pytest.raises(Exception) as exc_info:
        get(TEST_URL)

    assert 'An error occurred while requesting' in str(exc_info.value)


@pytest.mark.parametrize('status_code', [404, 403, 502, 503, 500])
def test__get__request_fails_with_http_status_error(
    mocker: MockFixture, status_code: int
):
    mock_request = mocker.Mock()
    mock_request.url = TEST_URL

    response = Response(status_code=status_code, request=mock_request)

    mocker.patch('httpx.get', return_value=response)

    with pytest.raises(Exception) as exc_info:
        get(TEST_URL)

    assert f'Error response {status_code} while requesting ' in str(
        exc_info.value
    )


async def test__async_get__request_successful(mocker: MockFixture):
    expected_result = {'key': 'value'}
    mock_response = mocker.Mock()
    mock_response.json.return_value = expected_result

    mock_get = mocker.AsyncMock(return_value=mock_response)
    mocker.patch.object(httpx.AsyncClient, 'get', mock_get)

    result = await async_get(TEST_URL)

    assert result == {'key': 'value'}
    mock_get.assert_called_once_with(TEST_URL)


async def test__async_get__request_fails_with_request_error(
    mocker: MockFixture,
):
    mock_request = mocker.Mock()
    mock_request.request.url = TEST_URL
    mocker.patch.object(
        httpx.AsyncClient,
        'get',
        side_effect=httpx.RequestError('Request error', request=mock_request),
    )

    with pytest.raises(Exception) as exc_info:
        await async_get(TEST_URL)

    assert 'An error occurred while requesting' in str(exc_info.value)


@pytest.mark.parametrize('status_code', [404, 403, 502, 503, 500])
async def test__async_get__request_fails_with_http_status_error(
    mocker: MockFixture, status_code: int
):
    mock_request = mocker.Mock()
    mock_request.url = TEST_URL

    response = Response(status_code=status_code, request=mock_request)

    mock_get = mocker.AsyncMock(return_value=response)

    mocker.patch.object(httpx.AsyncClient, 'get', mock_get)

    with pytest.raises(Exception) as exc_info:
        await async_get(TEST_URL)

    assert f'Error response {status_code} while requesting ' in str(
        exc_info.value
    )
