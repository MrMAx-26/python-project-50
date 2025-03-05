from gendiff.formatters import stylish
from gendiff.engine import get_diff, get_formatter
from gendiff.formatters import plain
from gendiff.formatters import json
from json import dumps, dump
import yaml
from gendiff import parser
import pytest


@pytest.fixture
def sample_diff():
    return {
        'key1': {'status': 'added', 'value': 'value1'},
        'key2': {'status': 'removed', 'value': 'value2'},
        'key3': {'status': 'changed', 'old_value': 'old_value3', 
            'new_value': 'new_value3'
        },
        'key4': {'status': 'unchanged', 'value': 'value4'},
        'key5': {'status': 'nested', 'value': {
            'nested_key1': {'status': 'added', 'value': 'nested_value1'},
            'nested_key2': {'status': 'unchanged', 'value': 'nested_value2'}
        }},
    }


def test_stylish_added(sample_diff):
    diff = {'key1': {'status': 'added', 'value': sample_diff['key1']['value']}}
    result = get_formatter(diff, 'stylish')
    expected_output = (
        "{\n"
        "  + key1: value1\n"
        "}"
    )
    assert result == expected_output


def test_stylish_removed(sample_diff):
    diff = {'key2': {'status': 'removed', 
        'value': sample_diff['key2']['value']}}
    result = get_formatter(diff, 'stylish')
    expected_output = (
        "{\n"
        "  - key2: value2\n"
        "}"
    )
    assert result == expected_output


def test_stylish_changed(sample_diff):
    diff = {
        'key3': {'status': 'changed',
            'old_value': sample_diff['key3']['old_value'],
            'new_value': sample_diff['key3']['new_value']
        },
        'key4': {'status': 'unchanged', 'value': sample_diff['key4']['value']}
    }
    result = get_formatter(diff, 'stylish')
    expected_output = (
        "{\n"
        "  - key3: old_value3\n"
        "  + key3: new_value3\n"
        "    key4: value4\n"
        "}"
    )
    assert result == expected_output


def test_stylish_nested(sample_diff):
    diff = {
        'key5': {'status': 'nested', 'value': sample_diff['key5']['value']},
        'key2': {'status': 'removed', 'value': sample_diff['key2']['value']}
    }
    result = get_formatter(diff, 'stylish')
    expected_output = (
        "{\n"
        "    key5: {\n"
        "      + nested_key1: nested_value1\n"
        "        nested_key2: nested_value2\n"
        "    }\n"
        "  - key2: value2\n"
        "}"
    )
    assert result == expected_output


@pytest.fixture
def sample_data():
    return {
        'file1': {'a': 1, 'b': 2, 'c': 3},
        'file2': {'a': 1, 'b': 2, 'd': 4},
        'file3': {'a': 1, 'b': {'x': 10, 'y': 20}},
        'file4': {'a': 1, 'b': {'x': 10, 'y': 30}},
    }


def test_get_diff_added():
    file1 = {'a': 1, 'b': 2}
    file2 = {'a': 1, 'b': 2, 'c': 3}
    expected = {
        'a': {'status': 'unchanged', 'value': 1},
        'b': {'status': 'unchanged', 'value': 2},
        'c': {'status': 'added', 'value': 3}
    }
    assert get_diff(file1, file2) == expected


def test_get_diff_removed(sample_data):
    file1 = sample_data['file1']
    file2 = {'a': 1, 'b': 2}
    expected = {
        'a': {'status': 'unchanged', 'value': 1},
        'b': {'status': 'unchanged', 'value': 2},
        'c': {'status': 'removed', 'value': 3}
    }
    assert get_diff(file1, file2) == expected


def test_get_diff_unchanged():
    file1 = {'a': 1, 'b': 2}
    file2 = {'a': 1, 'b': 2}
    expected = {
        'a': {'status': 'unchanged', 'value': 1},
        'b': {'status': 'unchanged', 'value': 2}
    }
    assert get_diff(file1, file2) == expected


def test_get_diff_changed():
    file1 = {'a': 1, 'b': 2}
    file2 = {'a': 1, 'b': 3}
    expected = {
        'a': {'status': 'unchanged', 'value': 1},
        'b': {
            'status': 'changed',
            'old_value': 2,
            'new_value': 3
        }
    }
    assert get_diff(file1, file2) == expected


def test_get_diff_complex(sample_data):
    file1 = sample_data['file1']
    file2 = sample_data['file2']
    expected = {
        'a': {'status': 'unchanged', 'value': 1},
        'b': {'status': 'unchanged', 'value': 2},
        'c': {'status': 'removed', 'value': 3},
        'd': {'status': 'added', 'value': 4}
    }
    assert get_diff(file1, file2) == expected


def test_get_diff_nested(sample_data):
    file1 = sample_data['file3']
    file2 = sample_data['file4']
    expected = {
        'a': {'status': 'unchanged', 'value': 1},
        'b': {
            'status': 'nested',
            'value': {
                'x': {'status': 'unchanged', 'value': 10}, 
                'y': {
                    'status': 'changed',
                    'old_value': 20,
                    'new_value': 30
                }
            }
        }
    }
    assert get_diff(file1, file2) == expected


def test_plain_added():
    diff = {
        'key1': {'status': 'added', 'value': 'new_value'},
        'key2': {'status': 'unchanged', 'value': 'old_value'},
    }
    result = get_formatter(diff, 'plain')
    expected_output = "Property 'key1' was added with value: 'new_value'"
    assert result == expected_output


def test_plain_removed():
    diff = {
        'key1': {'status': 'removed'},
        'key2': {'status': 'unchanged', 'value': 'old_value'},
    }
    result = get_formatter(diff, 'plain')
    expected_output = "Property 'key1' was removed"
    assert result == expected_output


def test_plain_changed():
    diff = {
        'key1': {'status': 'changed', 'old_value': 'old_value',
            'new_value': 'new_value'
        },
        'key2': {'status': 'unchanged', 'value': 'unchanged_value'},
    }
    result = get_formatter(diff, 'plain')
    expected_output = (
        "Property 'key1' was updated. From 'old_value' to 'new_value'"
    )
    assert result == expected_output


def test_plain_nested():
    diff = {
        'key1': {'status': 'nested', 'value': {
            'nested_key': {'status': 'added', 'value': 'nested_value'}
        }},
        'key2': {'status': 'unchanged', 'value': 'unchanged_value'},
    }
    result = get_formatter(diff, 'plain')
    expected_output = (
        "Property 'key1.nested_key' was added with value: 'nested_value'"
    )
    assert result == expected_output


@pytest.fixture
def file_pairs():
    return [
        (
            {'key1': 'value1'},
            {'key1': 'value1', 'key2': 'value2'},
            dumps({
                'key1': {'status': 'unchanged', 'value': 'value1'},
                'key2': {'status': 'added', 'value': 'value2'}
            }, indent=4)
        ),
        (
            {'key1': 'value1', 'key2': 'value2'},
            {'key1': 'value1'},
            dumps({
                'key1': {'status': 'unchanged', 'value': 'value1'},
                'key2': {'status': 'removed', 'value': 'value2'}
            }, indent=4)
        ),
        (
            {'key1': 'value1'},
            {'key1': 'value2'},
            dumps({
                'key1': {
                    'status': 'changed',
                    'old_value': 'value1',
                    'new_value': 'value2'
                }
            }, indent=4)
        ),
        (
            {'key1': {'subkey1': 'value1'}},
            {'key1': {'subkey1': 'value1', 'subkey2': 'value2'}},
            dumps({
                'key1': {
                    'status': 'nested',
                    'value': {
                        'subkey1': {'status': 'unchanged', 'value': 'value1'},
                        'subkey2': {'status': 'added', 'value': 'value2'}
                    }
                }
            }, indent=4)
        ),
        (
            {'key1': 'value1', 'key2': 'value2'},
            {'key1': 'value1', 'key2': 'value2'},
            dumps({
                'key1': {'status': 'unchanged', 'value': 'value1'},
                'key2': {'status': 'unchanged', 'value': 'value2'}
            }, indent=4)
        )
    ]


def test_get_json(file_pairs):
    for file1, file2, expected_output in file_pairs:
        diff = get_diff(file1, file2)
        result = get_formatter(diff, 'json')
        assert result == expected_output


def test_is_json():
    assert parser.is_json("file.json") is True
    assert parser.is_json("file.yml") is False
    assert parser.is_json("file.yaml") is False
    assert parser.is_json("file.txt") is False


def test_is_yaml():
    assert parser.is_yaml("file.yml") is True
    assert parser.is_yaml("file.yaml") is True
    assert parser.is_yaml("file.json") is False
    assert parser.is_yaml("file.txt") is False


@pytest.fixture
def json_file(tmp_path):
    data = {"key": "value"}
    json_file = tmp_path / "test.json"
    with open(json_file, 'w') as f:
        dump(data, f)
    return json_file


@pytest.fixture
def yaml_file(tmp_path):
    data = {"key": "value"}
    yaml_file = tmp_path / "test.yaml"
    with open(yaml_file, 'w') as f:
        yaml.dump(data, f)
    return yaml_file


def test_get_file_json(json_file):
    result = parser.get_file(json_file)
    assert result == {"key": "value"}


def test_get_file_yaml(yaml_file):
    result = parser.get_file(yaml_file)
    assert result == {"key": "value"}