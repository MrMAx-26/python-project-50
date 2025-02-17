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
    return args


def reading_and_parsing(file) -> dict:
    data = json.load(open(file))
    return data


def generate_diff(file1, file2) -> str:
    data1 = reading_and_parsing(file1)
    data2 = reading_and_parsing(file2)
    keys = sorted(set(data1.keys()).union(data2.keys()))
    diff = []
    for key in keys:
        if key in data1 and key in data2:
            if data1[key] != data2[key]:
                diff.append(f' - {key}: {data1[key]}')
                diff.append(f' + {key}: {data2[key]}')
            else:
                diff.append(f'   {key}: {data1[key]}')
        elif key in data1:
            diff.append(f' - {key}: {data1[key]}')
        elif key in data2:
            diff.append(f' + {key}: {data2[key]}')
    result_diff = '{\n' + '\n'.join(diff) + '\n}'
    return result_diff