from gendiff.formatters import stylish
from gendiff.engine import get_diff
import pytest


@pytest.fixture
def sample_diff():
    return {
        'key1': {'status': 'added', 'value': 'value1'},
        'key2': {'status': 'removed', 'value': 'value2'},
        'key3': {'status': 'changed', 'old_value': 'old_value3', 'new_value': 'new_value3'},
        'key4': {'status': 'unchanged', 'value': 'value4'},
        'key5': {'status': 'nested', 'value': {
            'nested_key1': {'status': 'added', 'value': 'nested_value1'},
            'nested_key2': {'status': 'unchanged', 'value': 'nested_value2'}
        }},
    }


def test_stylish_added(sample_diff):
    diff = {'key1': {'status': 'added', 'value': sample_diff['key1']['value']}}
    expected_output = (
        "{\n"
        "  + key1: value1\n"
        "}"
    )
    assert stylish.stylish(diff) == expected_output


def test_stylish_removed(sample_diff):
    diff = {'key2': {'status': 'removed', 'value': sample_diff['key2']['value']}}
    expected_output = (
        "{\n"
        "  - key2: value2\n"
        "}"
    )
    assert stylish.stylish(diff) == expected_output


def test_stylish_changed(sample_diff):
    diff = {
        'key3': {'status': 'changed', 'old_value': sample_diff['key3']['old_value'], 'new_value': sample_diff['key3']['new_value']},
        'key4': {'status': 'unchanged', 'value': sample_diff['key4']['value']}
    }
    expected_output = (
        "{\n"
        "  - key3: old_value3\n"
        "  + key3: new_value3\n"
        "    key4: value4\n"
        "}"
    )
    assert stylish.stylish(diff) == expected_output


def test_stylish_nested(sample_diff):
    diff = {
        'key5': {'status': 'nested', 'value': sample_diff['key5']['value']},
        'key2': {'status': 'removed', 'value': sample_diff['key2']['value']}
    }
    expected_output = (
        "{\n"
        "    key5: {\n"
        "      + nested_key1: nested_value1\n"
        "        nested_key2: nested_value2\n"
        "    }\n"
        "  - key2: value2\n"
        "}"
    )
    assert stylish.stylish(diff) == expected_output


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