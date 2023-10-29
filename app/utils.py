import json
from functools import wraps
from typing import Optional

from db.models import CityModel
from db.session import get_session
from pydantic._internal._model_construction import \
    ModelMetaclass as PydanticSchema
from settings import logger
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.decl_api import DeclarativeMeta as SQLAlchemy_Model


def log(mode):
    logger_modes = {
        'debug': logger.debug,
        'info': logger.info,
    }

    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            logger_modes[mode](f'start executing {func.__name__}')
            result = func(*args, **kwargs)
            logger_modes[mode](f'finished executing {func.__name__}')
            return result
        return inner
    return outer


@log('debug')
def bulk_insert_to_db(model: SQLAlchemy_Model, data: list[dict]) -> None:
    if not data:
        logger.debug('failed writing to database: got empty list')
        return
    try:
        with get_session() as session:
            session.execute(insert(model), data)
    except IntegrityError as err:
        logger.error('failed writing to database: %s', err)


def read_file(filename: str) -> dict:
    data = {}
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error('file not found: %s', filename)
    except json.JSONDecodeError:
        logger.error('invalid JSON file: %s', filename)

    return data


def validate_response(schema: PydanticSchema,
                      response: dict) -> Optional[dict]:
    try:
        valid_response = schema(**response)
    except ValueError as err:
        logger.error('response validation error: %s', err)
    else:
        return valid_response.model_dump()


def get_cities_list() -> list[CityModel]:
    with get_session() as session:
        cities = session.query(CityModel).all()
        session.expunge_all()
    return cities
