#!/usr/bin/env python

from gendiff import generate_diff
from gendiff.engine import reading_and_parsing, run_gendiff


def main():
    args = run_gendiff()
    print(reading_and_parsing(args.first_file))
    print(reading_and_parsing(args.second_file))
    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()