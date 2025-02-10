#!/usr/bin/env python

import argparse

def main():
    parser = argparse.ArgumentParser(
        usage='gendiff [-h] first_file second_file',
        description='Compares two configuration files and shows a difference.'
        )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main()