from gendiff import engine
import pytest
import json


@pytest.fixture
def temp_json_files(tmp_path):
    file1 = tmp_path / "test1.json"
    file2 = tmp_path / "test2.json"
    return file1, file2


def test_identical(temp_json_files):
    file1, file2 = temp_json_files
    data = {'key1': 'value1', 'key2': 'value2'}
    with open(file1, 'w') as f:
        json.dump(data, f)
    with open(file2, 'w') as f:
        json.dump(data, f)

    expected_output = '{\n   key1: value1\n   key2: value2\n}'
    assert engine.generate_diff(file1, file2) == expected_output


def test_diff(temp_json_files):
    file1, file2 = temp_json_files
    data1 = {'key1': 'value1', 'key2': 'value2'}
    data2 = {'key1': 'value1', 'key2': 'value3'}
    with open(file1, 'w') as f:
        json.dump(data1, f)
    with open(file2, 'w') as f:
        json.dump(data2, f)

    expected_output = '{\n   key1: value1\n - key2: value2\n + key2: value3\n}'
    assert engine.generate_diff(file1, file2) == expected_output


def test_missing_keys(temp_json_files):
    file1, file2 = temp_json_files
    data1 = {'key1': 'value1'}
    data2 = {'key2': 'value2'}
    with open(file1, 'w') as f:
        json.dump(data1, f)
    with open(file2, 'w') as f:
        json.dump(data2, f)

    expected_output = '{\n - key1: value1\n + key2: value2\n}'
    assert engine.generate_diff(file1, file2) == expected_output


def test_generate_key_diff_in_first():
    result = engine.generate_key_diff("key1", {"key1": "value1"}, {})

    expected_output = " - key1: value1"
    assert result == expected_output


def test_generate_key_diff_in_second():
    result = engine.generate_key_diff("key4", {}, {"key4": "value4"})

    expected_output = " + key4: value4"
    assert result == expected_output


def test_handle_common_key_equal_values():
    result = engine.handle_common_key("key3", "value3", "value3")

    expected_output = "   key3: value3"
    assert result == expected_output



def test_handle_common_key_different_values():
    result = engine.handle_common_key("key2", "value2", "value2_changed")

    expected_output = " - key2: value2\n + key2: value2_changed"
    assert result == expected_output