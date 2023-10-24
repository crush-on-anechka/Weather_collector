import datetime
import sys

import pytest

sys.path.append('app/')

from exceptions import BadResponseStatusException
from utils import read_file
from workers import CityFetcher, ForecastFetcher, WeatherFetcher


def test_get_api_response_valid_response_is_returned_as_dict(requests_mock):
    fetcher = WeatherFetcher(1, 1, 1, 1)
    expected = {'result': 'mock'}
    requests_mock.get(fetcher.url, json=expected, status_code=200)
    result = fetcher._get_api_response()
    assert result == expected


def test_get_api_response_invalid_response_returns_none(requests_mock):
    fetcher = WeatherFetcher(1, 1, 1, 1)
    requests_mock.get(fetcher.url, status_code=404)
    with pytest.raises(BadResponseStatusException):
        fetcher._get_api_response()


def test_weather_fetcher_process_response_returns_valid_data():
    fetcher = WeatherFetcher(1, 1, 1, 1)
    filename = 'app/tests/fixture_files/sample_weather.json'
    response = read_file(filename)
    result = fetcher._process_response(response)
    expected = [{
        'condition': 802,
        'temp': 283.49,
        'temp_min': 281.76,
        'temp_max': 285.47,
        'pressure': 1020,
        'humidity': 73,
        'wind_speed': 4.12,
        'wind_direction': 290,
        'wind_gust': None,
        'clouds': 40,
        'timestamp': datetime.datetime(
            1970, 1, 1, 0, 0, 1, tzinfo=datetime.timezone.utc),
        'city': 1
    }]
    assert result == expected


def test_forecast_fetcher_process_response_returns_valid_data():
    fetcher = ForecastFetcher(1, 1, 1, 1)
    filename = 'app/tests/fixture_files/sample_forecast.json'
    response = read_file(filename)
    assert isinstance(response, dict)
    assert 'list' in response
    assert 'cnt' in response
    assert response['cnt'] == len(response['list'])

    result = fetcher._process_response(response)
    expected = {
        'condition': 802,
        'temp': 285,
        'temp_min': 284.97,
        'temp_max': 285,
        'pressure': 1020,
        'humidity': 69,
        'wind_speed': 2.94,
        'wind_direction': 313,
        'wind_gust': 6.05,
        'clouds': 40,
        'timestamp': datetime.datetime(2023, 10, 14, 21, 0),
        'city': 1
    }
    assert result[0] == expected


def test_city_fetcher_process_response_returns_valid_data():
    fetcher = CityFetcher('city_name')
    filename = 'app/tests/fixture_files/sample_city_info.json'
    response = read_file(filename)
    result = fetcher._process_response(response)
    expected = [{
        'name': 'São Paulo',
        'latitude': -23.5506507,
        'longitude': -46.6333824,
        'country': 'BR',
        'state': 'São Paulo'
    }]
    assert result == expected


def test_city_fetcher_process_response_invalid_data_returns_empty_list():
    fetcher = CityFetcher('')
    result = fetcher._process_response({'invalid': 'response'})
    assert result == []


@pytest.mark.parametrize('prm', [({'invalid': 'response'}),
                                 ([{'invalid': 'response'}]),
                                 123,
                                 'invalid_response',
                                 None])
def test_weather_fetcher_process_response_invalid_data_returns_empty_list(prm):
    fetcher = WeatherFetcher(1, 1, 1, 1)
    result = fetcher._process_response(prm)
    assert result == []


@pytest.mark.parametrize('prm', [({'invalid': 'response'}),
                                 ([{'invalid': 'response'}]),
                                 123,
                                 'invalid_response',
                                 None])
def test_forecast_fetcher_process_response_invalid_data_return_empty_list(prm):
    fetcher = ForecastFetcher(1, 1, 1, 1)
    result = fetcher._process_response(prm)
    assert result == []
