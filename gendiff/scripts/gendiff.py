#!/usr/bin/env python

import argparse
from gendiff.engine import reading_and_parsing

def main():
    parser = argparse.ArgumentParser(
        usage='gendiff [-h] [-f FORMAT] first_file second_file',
        description='Compares two configuration files and shows a difference.'
        )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    print(reading_and_parsing(args.first_file))
    print(reading_and_parsing(args.second_file))


if __name__ == '__main__':
    main()