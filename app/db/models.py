from settings import CONSTR
from sqlalchemy import (CheckConstraint, Column, DateTime, Float, ForeignKey,
                        Integer, PrimaryKeyConstraint, String,
                        UniqueConstraint)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CityModel(Base):
    __tablename__ = 'cities'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    country = Column(String(2))
    state = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
    UniqueConstraint('name', 'country')
    CheckConstraint(
        f'{CONSTR["MIN_LAT_DEG"]} <= latitude AND '
        f'latitude <= {CONSTR["MAX_LAT_DEG"]}',
        name='lat_check')
    CheckConstraint(
        f'{CONSTR["MIN_LON_DEG"]} <= longitude AND '
        f'longitude <= {CONSTR["MAX_LON_DEG"]}',
        name='lon_check')


class ConditionModel(Base):
    __tablename__ = 'conditions'

    id = Column(Integer, primary_key=True)
    main = Column(String(20))
    description = Column(String(50))


class WeatherModel(Base):
    __abstract__ = True

    timestamp = Column(DateTime, primary_key=True)
    temp = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    wind_direction = Column(Integer)
    wind_gust = Column(Float)
    clouds = Column(Integer)
    city = Column(ForeignKey('cities.id', ondelete='CASCADE'))
    condition = Column(ForeignKey('conditions.id', ondelete='RESTRICT'))
    PrimaryKeyConstraint('timestamp', 'city')
    CheckConstraint(
        f'{CONSTR["MIN_TEMP_KELVIN"]} < temp AND '
        f'temp < {CONSTR["MAX_TEMP_KELVIN"]}',
        name='temp_check')
    CheckConstraint(
        f'{CONSTR["MIN_TEMP_KELVIN"]} < temp_min AND '
        f'temp_min < {CONSTR["MAX_TEMP_KELVIN"]}',
        name='min_temp_check')
    CheckConstraint(
        f'{CONSTR["MIN_TEMP_KELVIN"]} < temp_max AND '
        f'temp_max < {CONSTR["MAX_TEMP_KELVIN"]}',
        name='max_temp_check')
    CheckConstraint(
        f'{CONSTR["MIN_PRESSURE_HPA"]} < pressure AND '
        f'pressure < {CONSTR["MAX_PRESSURE_HPA"]}',
        name='pressure_check')
    CheckConstraint(
        f'{CONSTR["MIN_HUMIDITY_PERC"]} <= humidity AND '
        f'humidity <= {CONSTR["MAX_HUMIDITY_PERC"]}',
        name='humidity_check')
    CheckConstraint(
        f'{CONSTR["MIN_CLOUDNESS_PERC"]} <= clouds AND '
        f'clouds <= {CONSTR["MAX_CLOUDNESS_PERC"]}',
        name='clouds_check')
    CheckConstraint(
        f'{CONSTR["MIN_WIND_SPEED_M_SEC"]} <= wind_speed AND '
        f'wind_speed < {CONSTR["MAX_WIND_SPEED_M_SEC"]}',
        name='wind_speed_check')
    CheckConstraint(
        f'{CONSTR["MIN_WIND_DIR_DEG"]} <= wind_direction AND '
        f'wind_direction <= {CONSTR["MAX_WIND_DIR_DEG"]}',
        name='wind_dir_check')
    CheckConstraint(
        f'{CONSTR["MIN_WIND_GUST_M_SEC"]} <= wind_gust AND '
        f'wind_gust < {CONSTR["MAX_WIND_GUST_M_SEC"]}',
        name='wind_gust_check')


class WeatherFactModel(WeatherModel):
    __tablename__ = 'weather_fact'


class WeatherForecastModel(WeatherModel):
    __tablename__ = 'weather_forecast'
