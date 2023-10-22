import sys

sys.path.append('app/')

from db.schemas import ConditionSchema
from utils import read_file, validate_response


def test_validate_response_valid_input_returns_dict():
    valid_response = {
        'id': 200,
        'main': 'Thunderstorm',
        'description': 'thunderstorm with light rain'
    }
    result = validate_response(ConditionSchema, valid_response)
    assert result == valid_response


def test_validate_response_invalid_input_returns_none():
    invalid_response = {}

    result = validate_response(ConditionSchema, invalid_response)
    assert result is None


def test_read_file_valid_input_returns_nonempty_dict():
    filename = 'app/tests/fixture_files/sample_weather.json'
    result = read_file(filename)
    assert isinstance(result, dict)
    assert bool(len(result))


def test_read_file_invalid_input_returns_empty_dict():
    filename = ''
    result = read_file(filename)
    assert result == {}
