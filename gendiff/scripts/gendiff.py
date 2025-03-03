#!/usr/bin/env python

from gendiff.cli import parse_args
from gendiff.generate_diff import generate_diff


def main():
    args = parse_args()
    format_diff = generate_diff(args.first_file, args.second_file, args.format)
    print(format_diff)


if __name__ == '__main__':
    main()