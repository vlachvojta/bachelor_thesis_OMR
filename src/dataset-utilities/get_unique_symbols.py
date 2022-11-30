#!/usr/bin/python3.8

import argparse
import re
import sys
import os
import pandas as pd

from common import Common


class Get_unique_symbols:
    """Open file(s) and extract all unique music symbol ids."""

    file_names = []

    # Dictionary of Pandas series. Key = symbol type
    unique_symbols = {}

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

        file_data = self.read_file(file)
        if not file_data:
            return

        symbols = re.split(r'\s', file_data)

        unique_symbols = {}

        for sym in symbols:
            if not sym:
                continue

            col = re.split(r'-|\.', sym)[0]

            if col in list(unique_symbols.keys()):
                unique_symbols[col].add(sym)
            else:
                unique_symbols[col] = {sym}

        print('unique_symbols:')
        print(unique_symbols)

        for col in list(unique_symbols.keys()):
            if col in self.unique_symbols.keys():
                self.unique_symbols[col].update(unique_symbols[col])
            else:
                self.unique_symbols[col] = unique_symbols[col]
        print('self.unique_symbols:')
        print(self.unique_symbols)

        return

    def read_file(self, file: str):
        """Read file, method assumes, file exists."""
        with open(file) as f:
            data = f.read()
        return data

    def finalize(self):
        # print('\n' + '========================' * 3 + '\n')
        # self.print_symbols()

        print('\n' + '========================' * 3 + '\n')
        self.print_symbols()

    def print_symbols(self):
        Common.print_dict(self.unique_symbols)


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
    gus.finalize()


if __name__ == "__main__":
    main()
