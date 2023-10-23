import os
import time
from sys import argv
from typing import Optional

from apscheduler.schedulers.blocking import BlockingScheduler
from db.models import (CityModel, ConditionModel, WeatherFactModel,
                       WeatherForecastModel)
from db.schemas import ConditionSchema
from db.session import get_session
from settings import FETCH_INTERVAL_SEC, logger
from sqlalchemy import delete
from utils import (bulk_insert_to_db, get_cities_list, log, read_file,
                   validate_response)
from workers import CityFetcher, ForecastFetcher, WeatherFetcher


@log('info')
def load_cities() -> None:
    data: dict = read_file('cities.json')
    cities_data = []
    for city in data:
        city_data = CityFetcher(city_name=city).run
        if city_data:
            cities_data.extend(city_data)
    logger.info('got data for %d of %d cities', len(cities_data), len(data))
    bulk_insert_to_db(CityModel, cities_data)


@log('info')
def load_conditions() -> None:
    data: dict = read_file('conditions.json')
    condition_models: list[Optional[dict]] = [
        validate_response(ConditionSchema, i) for i in data]
    bulk_insert_to_db(ConditionModel, condition_models)


@log('info')
def fetch_weather(cities) -> None:
    cur_time = time.time()

    weather_data, forecast_data = [], []
    for c in cities:
        if not c.latitude or not c.longitude:
            continue
        weather_data.extend(
            WeatherFetcher(cur_time, c.id, c.latitude, c.longitude).run)
        forecast_data.extend(
            ForecastFetcher(cur_time, c.id, c.latitude, c.longitude).run)

    logger.info('got weather data for %d of %d cities',
                len(weather_data), len(cities))

    session = next(get_session())
    with session.begin():
        session.execute(delete(WeatherForecastModel))

    bulk_insert_to_db(WeatherForecastModel, forecast_data)
    bulk_insert_to_db(WeatherFactModel, weather_data)


def main() -> None:
    load_conditions()
    load_cities()

    cities = get_cities_list()
    fetch_weather(cities)

    scheduler = BlockingScheduler()
    scheduler.add_job(
        fetch_weather, 'interval', [cities], seconds=FETCH_INTERVAL_SEC)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def launcher() -> None:
    param = ' '.join(argv[1:])
    if param not in START_OPTIONS:
        logger.critical('''Invalid starting option. Use one of the following:
                        python main.py --load cities
                                       --load conditions
                                       --start program''')
        return

    logger.info(f'launching {param}')
    START_OPTIONS[param]()


if __name__ == '__main__':
    START_OPTIONS = {
        '--load cities': load_cities,
        '--load conditions': load_conditions,
        '--start program': main,
    }
    launcher()
