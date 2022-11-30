#!/usr/bin/python3.8

import argparse
import re
import sys
import os
from common import Common


class Get_unique_symbols:
    """Open file(s) and extract all unique music symbol ids."""

    file_names = []

    # Dictionary of Pandas series. Key = symbol type
    unique_symbols = {}

    def __init__(self, files: list = [], dirs: str = '',
                 exts: str = '', recursive: bool = False):
        if recursive:
            print("Recursive lookup has NOT been implemented yet!!!",
                  file=sys.stderr)

        self.file_names = Common.get_existing_file_names(files, dirs,
                                                         exts, recursive)
        print(self.file_names)
        for file in self.file_names:
            self.get_symbols_from_file(file)

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

    def finalize(self, file='stdout'):
        if file == 'stdout':
            print('\n' + '========================' * 3 + '\n')
            self.print_symbols()
        else:
            print('This type of output has NOT been implemented yet.',
                  file=sys.stderr)

    def print_symbols(self):
        Common.print_dict(self.unique_symbols)


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--files", nargs='*',
        help=("Files to read symbols from, you can add more files.\n" +
              "USE FULL FILE PATH (relative or absolute)"))
    parser.add_argument(
        "-e", "--extensions", nargs='*', default=['semantic', 'agnostic'],
        help=("Set file extensions for files in given folder\n" +
              "Use in combination with --directories."))
    parser.add_argument(
        "-d", "--directories", nargs='*', default=[],
        help=("Directories where to look for files with given extensions. \n" +
              "Use in combination with --extensions."))
    # parser.add_argument(
    #     "-r", "--recursive", default=False, action='store_true',
    #     help=("Activate recursive search in given directory.\n" +
    #           "If not set, use only files in given directory"))
    parser.add_argument(
        "-o", "--output", default='stdout',
        help="Set output file with extension. Output format is JSON")

    # parser.add_argument(
    #     "-o", "--out", default='',
    #     help="Set output file, stdout by default")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    gus = Get_unique_symbols(
        files=args.files,
        dirs=args.directories,
        exts=args.extensions)
    gus.finalize(args.output)
    # gus.print_symbols(args.out)


if __name__ == "__main__":
    main()
