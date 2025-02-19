import argparse
import json


def run_gendiff():
    parser = argparse.ArgumentParser(
        usage='gendiff [-h] [-f FORMAT] first_file second_file',
        description='Compares two configuration files and shows a difference.'
        )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    print_diff(args)


def print_diff(args):
    print(generate_diff(args.first_file, args.second_file))


def reading_and_parsing(file) -> dict:
    data = json.load(open(file))
    return data


def generate_diff(file1, file2) -> str:
    data1 = reading_and_parsing(file1)
    data2 = reading_and_parsing(file2)
    keys = sorted(set(data1.keys()).union(data2.keys()))
    diff = []
    for key in keys:
        diff.append(generate_key_diff(key, data1, data2))
    result_diff = '{\n' + '\n'.join(diff) + '\n}'
    return result_diff


def generate_key_diff(key, data1, data2) -> str:
    if key in data1 and key in data2:
        return handle_common_key(key, data1[key], data2[key])
    elif key in data1:
        return f' - {key}: {data1[key]}'
    elif key in data2:
        return f' + {key}: {data2[key]}'
    return ''


def handle_common_key(key, value1, value2) -> str:
    if value1 != value2:
        return f' - {key}: {value1}\n + {key}: {value2}'
    return f'   {key}: {value1}'