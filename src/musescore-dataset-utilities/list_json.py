#!/usr/bin/python3.8

import json
import re
import argparse

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "poly_file", type=str,
        help="File with json list of polyphonic parts in that directory.")
    parser.add_argument(
        "-m", "--mode", type=str, default='whole', choices=['whole', 'short', 'orig_musicxml'],
        help="Input mode of output of the files. (just simple str operations)")
    return parser.parse_args()


def main():

    args = parseargs()

    with open(args.poly_file, 'r') as f:
        data = json.load(f)

    for p in data:
        if args.mode == 'whole':
            print(p)
        elif args.mode == 'short':
            number = re.split(r'_', p)[0]
            print(number)
        elif args.mode == 'orig_musicxml':
            number = re.split(r'_', p)[0]
            print(f'{number}.musicxml')


if __name__ == '__main__':
    main()
