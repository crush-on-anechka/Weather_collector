import json
import time
from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import datetime as dt
from typing import Optional

import requests
from db.schemas import CitySchema, WeatherSchema
from requests.exceptions import ConnectionError, ReadTimeout
from settings import (API_KEY, CITY_DATA_BASE_URL, FORECAST_BASE_URL,
                      MAX_REQUEST_RETRIES, REQUEST_TIMEOUT, WEATHER_BASE_URL,
                      logger)
from utils import log, validate_response


class Fetcher(ABC):
    def __init__(self, timestamp: Optional[float] = None,
                 city_id: Optional[int] = None,
                 lat: Optional[float] = None,
                 lon: Optional[float] = None,
                 params: Optional[dict] = None,
                 city_name: Optional[str] = None) -> None:
        self.timestamp = timestamp
        self.city_name = city_name
        self.city_id = city_id
        self.params = {
            'appid': API_KEY,
            'lat': lat,
            'lon': lon
        }

    @log('debug')
    def _get_api_response(self) -> Optional[dict]:
        logger.debug('sending request to %s with parameters: %s',
                     self.url, self.params)

        retry_counter = MAX_REQUEST_RETRIES
        while retry_counter:
            try:
                response = requests.get(url=self.url, params=self.params)
                break
            except (ReadTimeout, ConnectionError) as err:
                error_data = err
                retry_counter -= 1
                if retry_counter:
                    time.sleep(REQUEST_TIMEOUT)
                logger.debug('request error at: %s, %d tries left, info: %s',
                             self.url, retry_counter, error_data)

        if not retry_counter:
            logger.error('request error at: %s, %s', self.url, error_data)
            return None

        logger.debug(f'response {response.status_code} from {self.url}')
        if response.ok:
            return json.loads(response.text)

        logger.error('Bad response status %d at: %s',
                     response.status_code, self.url)

    def _construct_mapping(self, item: dict) -> dict:
        if not isinstance(item, Iterable):
            return {}

        processed_response = {
            'city': self.city_id
        }

        if 'weather' in item:
            w = item['weather']
            if w and isinstance(w, list):
                processed_response['condition'] = w[0].get('id')

        if 'main' in item:
            m = item['main']
            processed_response['temp'] = m.get('temp')
            processed_response['temp_min'] = m.get('temp_min')
            processed_response['temp_max'] = m.get('temp_max')
            processed_response['pressure'] = m.get('pressure')
            processed_response['humidity'] = m.get('humidity')

        if 'wind' in item:
            w = item['wind']
            processed_response['wind_speed'] = w.get('speed')
            processed_response['wind_direction'] = w.get('deg')
            processed_response['wind_gust'] = w.get('gust')

        if 'clouds' in item:
            processed_response['clouds'] = item['clouds'].get('all')

        if 'dt' in item:
            processed_response['timestamp'] = dt.fromtimestamp(item['dt'])

        return processed_response

    @abstractmethod
    def _process_response(self, response) -> list[Optional[dict]]:
        pass

    @property
    def run(self) -> list[Optional[dict]] | None:
        response: Optional[dict] = self._get_api_response()
        if response:
            processed_response: list[
                Optional[dict]] = self._process_response(response)
            return processed_response


class CityFetcher(Fetcher):
    def __init__(self, city_name: str) -> None:
        self.url = CITY_DATA_BASE_URL
        self.params = {
            'appid': API_KEY,
            'q': city_name
        }

    def _process_response(self, response: list[dict]) -> list[Optional[dict]]:
        try:
            processed_response = response[0]
        except (TypeError, IndexError, KeyError) as err:
            logger.error('processing response failed: %s: %s',
                         type(err), *err.args)
        else:
            if 'local_names' in processed_response:
                processed_response.pop('local_names')
            valid_response: Optional[dict] = validate_response(
                CitySchema, processed_response)
            return [valid_response]


class WeatherFetcher(Fetcher):
    def __init__(self, timestamp: float, city_id: int, lat: float, lon: float,
                 params: Optional[dict] = None) -> None:
        super().__init__(timestamp, city_id, lat, lon, params)
        self.url = WEATHER_BASE_URL

    def _process_response(self, response: dict) -> list[Optional[dict]]:
        processed_response: dict = self._construct_mapping(response)
        processed_response['timestamp'] = self.timestamp
        valid_response: Optional[dict] = validate_response(
            WeatherSchema, processed_response)
        return [valid_response]


class ForecastFetcher(Fetcher):
    def __init__(self, timestamp: float, city_id: int, lat: float, lon: float,
                 params: Optional[dict] = None) -> None:
        super().__init__(timestamp, city_id, lat, lon, params)
        self.url = FORECAST_BASE_URL

    def _process_response(self, response: dict) -> list[Optional[dict]]:
        items = []
        try:
            response_items: list[dict] = response['list']
        except (AttributeError, TypeError, KeyError) as err:
            logger.error('processing response failed: %s: %s',
                         type(err), *err.args)
        else:
            for item in response_items:
                processed_response: dict = self._construct_mapping(item)
                valid_item: Optional[dict] = validate_response(
                    WeatherSchema, processed_response)
                items.append(valid_item)

        return items
