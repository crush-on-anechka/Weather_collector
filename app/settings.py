import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY')
MAX_REQUEST_RETRIES = 3
FETCH_INTERVAL_SEC = 3600
REQUEST_TIMEOUT = 5

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
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
