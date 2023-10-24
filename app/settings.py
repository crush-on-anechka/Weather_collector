import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY')
MAX_REQUEST_RETRIES = 3
FETCH_INTERVAL_SEC = 3600
REQUEST_TIMEOUT = 5

# CONSTRAINTS
CONSTR = {
    'MIN_LAT_DEG': -90,
    'MAX_LAT_DEG': 90,
    'MIN_LON_DEG': -180,
    'MAX_LON_DEG': 180,
    'MIN_TEMP_KELVIN': 100,
    'MAX_TEMP_KELVIN': 400,
    'MIN_PRESSURE_HPA': 0,
    'MAX_PRESSURE_HPA': 2000,
    'MIN_HUMIDITY_PERC': 0,
    'MAX_HUMIDITY_PERC': 100,
    'MIN_CLOUDNESS_PERC': 0,
    'MAX_CLOUDNESS_PERC': 100,
    'MIN_WIND_SPEED_M_SEC': 0,
    'MAX_WIND_SPEED_M_SEC': 1000,
    'MIN_WIND_DIR_DEG': 0,
    'MAX_WIND_DIR_DEG': 360,
    'MIN_WIND_GUST_M_SEC': 0,
    'MAX_WIND_GUST_M_SEC': 1000,
}

# DATABASE
DB = os.environ.get('POSTGRES_DB')
USER = os.environ.get('POSTGRES_USER')
PASS = os.environ.get('POSTGRES_PASSWORD')
DATABASE_URL = f'postgresql://{USER}:{PASS}@db:5432/{DB}'

# API URLs
BASE_URL = 'http://api.openweathermap.org/data/2.5/'
WEATHER_BASE_URL = BASE_URL + 'weather'
FORECAST_BASE_URL = BASE_URL + 'forecast'
CITY_DATA_BASE_URL = 'http://api.openweathermap.org/geo/1.0/direct'

# logger settings
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
