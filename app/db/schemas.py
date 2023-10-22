from datetime import datetime
from typing import Optional

from pydantic import (BaseModel, Field, ValidationInfo, field_validator,
                      model_validator)


class CitySchema(BaseModel):
    name: str
    country: Optional[str]
    latitude: float = Field(alias="lat")
    longitude: float = Field(alias="lon")
    state: Optional[str] = None

    @field_validator('country')
    @classmethod
    def country_valid_length(cls, v: str) -> str:
        if v and len(v) != 2:
            raise ValueError('value for "country" must consist of two symbols')
        return v

    @field_validator('latitude')
    @classmethod
    def latitude_valid_range(cls, v: float) -> float:
        if not -90 <= v <= 90:
            raise ValueError('latitude must be in range from -90 to 90')
        return v

    @field_validator('longitude')
    @classmethod
    def longitude_valid_range(cls, v: float) -> float:
        if not -180 <= v <= 180:
            raise ValueError('longitude must be in range from -180 to 180')
        return v


class ConditionSchema(BaseModel):
    id: int
    main: str
    description: str


class WeatherSchema(BaseModel):
    timestamp: datetime
    temp: Optional[float]
    temp_min: Optional[float]
    temp_max: Optional[float]
    pressure: Optional[int]
    humidity: Optional[int]
    wind_speed: Optional[float]
    wind_direction: Optional[int]
    wind_gust: Optional[float]
    clouds: Optional[int]
    city: int
    condition: Optional[int]

    @model_validator(mode='after')
    def check_if_temp_info_presence(self) -> 'WeatherSchema':
        if not (self.temp or self.temp_min or self.temp_max):
            raise ValueError('data must contain temperature information')
        return self

    @field_validator('temp', 'temp_min', 'temp_max')
    @classmethod
    def temp_valid_range(cls, v: float, info: ValidationInfo) -> float:
        if v and not 100 < v < 400:
            raise ValueError(
                f'invalid temperature value for field {info.field_name}')
        return v

    @field_validator('wind_speed', 'wind_gust')
    @classmethod
    def wind_valid_range(cls, v: float, info: ValidationInfo) -> float:
        if v and not 0 <= v < 1000:
            raise ValueError(
                f'invalid value for field {info.field_name}')
        return v

    @field_validator('pressure')
    @classmethod
    def pressure_valid_range(cls, v: int) -> int:
        if v and not 0 < v < 2000:
            raise ValueError('invalid pressure value')
        return v

    @field_validator('humidity')
    @classmethod
    def humidity_valid_range(cls, v: int) -> int:
        if v and not 0 <= v <= 100:
            raise ValueError('invalid humidity value')
        return v

    @field_validator('wind_direction')
    @classmethod
    def wind_direction_valid_range(cls, v: int) -> int:
        if v and not 0 <= v <= 360:
            raise ValueError('invalid wind direction value')
        return v

    @field_validator('clouds')
    @classmethod
    def clouds_valid_range(cls, v: int) -> int:
        if v and not 0 <= v <= 100:
            raise ValueError('invalid clouds value')
        return v
