#!/usr/bin/python3.8

import argparse
import re
import sys
import os


class Get_unique_symbols:
    """Open file(s) and extract all unique music symbol ids."""

    file_names = []
    data = {}

    def __init__(self, dir: str = '', ext: str = '', files: list = []):
        self.file_names = self.get_file_names(dir, ext)

    def get_file_names(self, dir, ext) -> list:
        """Get file names from directory with given extension

        Or all files in indirectory, if ext is empty."""
        if not dir:
            return []

        os.listdir(dir)

    def get_symbols_from_file(self, file: str):
        print('getting things from file', file)

        data = self.read_file(file)
        if not data:
            return

        symbols = re.split(r'\s', data)

        for sym in symbols:
            if not sym:
                continue

            type = re.split(r'-|\.', sym)[0]

            if type in list(self.data.keys()):
                self.data[type].add(sym)
            else:
                self.data[type] = {sym}

        return

    def read_file(self, file: str):
        """Read file, method assumes, file exists."""
        with open(file) as f:
            data = f.read()
        return data

    def print_symbols(self):
        self.print_dir(self.data)

    def print_dir(self, data: dict):
        print('{')
        print(list(data.keys()))
        for key in list(data.keys()):
            print(f'\t{key}: {data[key]}')
        print('}')


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", action='append',
        help="File to read symbols from, you can add more files")
    parser.add_argument(
        "-e", "--ext", default='semantic', action='append',
        help=(f"Set file extension for files in given folder\n" +
              f"Use in combination with --directory."))
    parser.add_argument(
        "-d", "--dir", default='', action='append',
        help=(f"Directory where to look for files with correct extension\n" +
              f"Use in combination with --ext."))
    # parser.add_argument(
    #     "-o", "--out", default='',
    #     help="Set output file, stdout by default")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    gus = Get_unique_symbols(dir=args.dir, ext=args.ext, files=args.file)

    for f in args.file:
        gus.get_symbols_from_file(f)

    # gus.print_symbols(args.out)
    gus.print_symbols()


if __name__ == "__main__":
    main()
