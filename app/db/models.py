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
    CheckConstraint('-90 <= latitude AND latitude <= 90', name='lat_check')
    CheckConstraint('-180 <= longitude AND longitude <= 180', name='lon_check')


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
    CheckConstraint('100 < temp AND temp < 400', name='temp_check')
    CheckConstraint('100 < temp_min AND temp_min < 400', name='min_temp_check')
    CheckConstraint('100 < temp_max AND temp_max < 400', name='max_temp_check')
    CheckConstraint('0 < pressure AND pressure < 2000', name='pressure_check')
    CheckConstraint('0 <= humidity AND humidity <= 100', name='humidity_check')
    CheckConstraint('0 <= clouds AND clouds <= 100', name='clouds_check')
    CheckConstraint(
        '0 <= wind_speed AND wind_speed < 1000', name='wind_speed_check')
    CheckConstraint(
        '0 <= wind_direction AND wind_direction <= 360', name='wind_dir_check')
    CheckConstraint(
        '0 <= wind_gust AND wind_gust < 1000', name='wind_gust_check')


class WeatherFactModel(WeatherModel):
    __tablename__ = 'weather_fact'


class WeatherForecastModel(WeatherModel):
    __tablename__ = 'weather_forecast'
