import json
import time
from abc import ABC, abstractmethod
from datetime import datetime as dt
from typing import Optional

import requests
from db.schemas import CitySchema, WeatherSchema
from exceptions import APIConnectionException, BadResponseStatusException
from requests.exceptions import ConnectionError, MissingSchema, ReadTimeout
from settings import (API_KEY, CITY_DATA_BASE_URL, FORECAST_BASE_URL,
                      MAX_REQUEST_RETRIES, REQUEST_TIMEOUT_SEC,
                      WEATHER_BASE_URL, logger)
from utils import log, validate_response


class Fetcher(ABC):
    def __init__(self, timestamp: Optional[float] = None,
                 city_id: Optional[int] = None,
                 lat: Optional[float] = None,
                 lon: Optional[float] = None,
                 city_name: Optional[str] = None) -> None:
        self.timestamp = timestamp
        self.city_name = city_name
        self.city_id = city_id
        self.request_timeout = REQUEST_TIMEOUT_SEC
        self.params = {
            'appid': API_KEY,
            'lat': lat,
            'lon': lon
        }

    @log('debug')
    def _get_api_response(self) -> dict:
        logger.debug('sending request to %s with parameters: %s',
                     self.url, self.params)

        retry_counter = MAX_REQUEST_RETRIES
        while retry_counter:
            try:
                response = requests.get(url=self.url, params=self.params)
                break
            except (ConnectionError, MissingSchema, ReadTimeout) as err:
                error_data = err
                retry_counter -= 1
                if retry_counter:
                    time.sleep(self.request_timeout)

        if not retry_counter:
            logger.debug('request error at: %s, %s', self.url, error_data)
            raise APIConnectionException

        logger.debug(f'response {response.status_code} from {self.url}')
        if response.ok:
            return json.loads(response.text)

        logger.debug('Bad response status %d at: %s',
                     response.status_code, self.url)
        raise BadResponseStatusException

    def _construct_mapping(self, item: dict) -> dict:
        if not isinstance(item, dict):
            logger.debug('invalid response type from %s', self.url)
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
    def _process_response(self, response) -> list[dict]:
        pass

    @property
    def run(self) -> list[dict]:
        try:
            response: dict = self._get_api_response()
        except (APIConnectionException, BadResponseStatusException) as err:
            logger.error('API response error: %s', err)
        else:
            processed_response: list[dict] = self._process_response(response)
            return processed_response

        return []


class CityFetcher(Fetcher):
    def __init__(self, city_name: str) -> None:
        self.url = CITY_DATA_BASE_URL
        self.params = {
            'appid': API_KEY,
            'q': city_name
        }

    def _process_response(self, response: list[dict]) -> list[dict]:
        try:
            if isinstance(response, list):
                processed_response = response[0]
        except IndexError as err:
            logger.error('processing response failed: %s', err)
        else:
            if 'local_names' in processed_response:
                processed_response.pop('local_names')
            valid_response: Optional[dict] = validate_response(
                CitySchema, processed_response)
            return [valid_response] if valid_response else []

        return []


class WeatherFetcher(Fetcher):
    def __init__(self, timestamp: float, city_id: int,
                 lat: float, lon: float) -> None:
        super().__init__(timestamp, city_id, lat, lon)
        self.url = WEATHER_BASE_URL

    def _process_response(self, response: dict) -> list[dict]:
        processed_response: dict = self._construct_mapping(response)
        processed_response['timestamp'] = self.timestamp
        valid_response: Optional[dict] = validate_response(
            WeatherSchema, processed_response)
        return [valid_response] if valid_response else []


class ForecastFetcher(Fetcher):
    def __init__(self, timestamp: float, city_id: int,
                 lat: float, lon: float) -> None:
        super().__init__(timestamp, city_id, lat, lon)
        self.url = FORECAST_BASE_URL

    def _process_response(self, response: dict) -> list[dict]:
        items = []
        try:
            response_items: list[dict] = response['list']
        except (TypeError, KeyError) as err:
            logger.error('processing response failed: %s', err)
        else:
            for item in response_items:
                processed_response: dict = self._construct_mapping(item)
                if not processed_response:
                    continue
                valid_item: Optional[dict] = validate_response(
                    WeatherSchema, processed_response)
                if valid_item:
                    items.append(valid_item)

        return items
