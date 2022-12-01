#!/usr/bin/python3.8

import argparse
import re
import sys
import os
from common import Common
import time


class Get_unique_symbols:
    """Open file(s) and extract all unique music symbol ids."""

    file_names = []

    # Dictionary of Pandas series. Key = symbol type
    unique_symbols = {}

    def __init__(self, files: list = [], exts: list = 'semantic',
                 folders: str = ['.'], recursive: bool = False,
                 database: str = 'all_unique_symbols.json',
                 input_file: str = 'files.txt'):
        # if recursive:
        #     print("Recursive lookup has NOT been implemented yet!!!",
        #           file=sys.stderr)
        # self.file_names = Common.get_existing_file_names(files, dirs,
        #                                                  exts, recursive)
        print('Hello from GET_UNIQUE_SYMBOLS')
        self.load_start_data(database)
        loaded_symbols_sum = self.count_unique_symbols()

        for folder in folders:
            files += Common.get_files(folder, exts)

        files += Common.get_lines(input_file)
        files = list(set(files))
        self.file_names = Common.check_existing_files(files)

        # self.unique_symbols['files'] = self.file_names
        print(f'Getting data from {len(self.file_names)} files '
              f'(every dot is 1000 parsed file).')

        for i, file in enumerate(self.file_names):
            if i % 1000 == 0:
                print('.', end='')
                sys.stdout.flush()
            self.get_symbols_from_file(file)
        print('')

        total_symbols = self.count_unique_symbols()
        new_symbols_count = total_symbols - loaded_symbols_sum
        print(f'{new_symbols_count} new symbols discovered. '
              f'({total_symbols} total)')

    def load_start_data(self, file):
        db = Common.read_file(file)
        # print(type(db))
        # print(type(db[list(db.keys())[0]]))
        # print(db[list(db.keys())[0]])

        # Check if data has correct format
        if isinstance(db, dict):
            types = [k for k in list(db.keys()) if not isinstance(db[k], list)]
            if types == []:
                for k, v in db.items():
                    self.unique_symbols[k] = set(v)

    def get_symbols_from_file(self, file: str):
        """Get symbols, save or append to `self.unique_symbols`."""
        file_data = Common.read_file(file)
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

        for col in list(unique_symbols.keys()):
            if col in self.unique_symbols.keys():
                try:
                    self.unique_symbols[col].update(unique_symbols[col])
                except AttributeError:
                    self.unique_symbols[col] = set(self.unique_symbols[col])
                    self.unique_symbols[col].update(unique_symbols[col])
            else:
                self.unique_symbols[col] = unique_symbols[col]

    def count_unique_symbols(self):
        """Return sum of all unique symbols found."""
        sum = 0
        for key in list(self.unique_symbols.keys()):
            sum += len(self.unique_symbols[key])
        return sum

    def finalize(self, file='stdout'):
        for key in list(self.unique_symbols.keys()):
            self.unique_symbols[key] = list(self.unique_symbols[key])

        if file == 'stdout':
            print('\n' + '========================' * 3 + '\n')
            self.print_symbols()
        else:
            Common.save_dict_as_json(self.unique_symbols, file)

    def print_symbols(self):
        Common.print_dict(self.unique_symbols, files=True)


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--files", nargs='*', default=[],
        help=("Files to read symbols from, you can add more files.\n" +
              "USE FULL FILE PATH (relative or absolute)"))
    parser.add_argument(
        "-e", "--extensions", nargs='*', default=['semantic'],#,  'agnostic'],
        help=("Set file extensions for files in given folder\n" +
              "Use in combination with --directories."))
    parser.add_argument(
        "-F", "--folders", nargs='*', default=['.'],
        help=("Directories where to look for files with given extensions. \n" +
              "Use in combination with --extensions."))
    # parser.add_argument(
    #     "-r", "--recursive", default=False, action='store_true',
    #     help=("Activate recursive search in given directory.\n" +
    #           "If not set, use only files in given directory"))
    parser.add_argument(
        "-d", "--database", default="all_unique_symbols.json",
        help="Database with already found unique_symbols.")
    parser.add_argument(
        "-o", "--output", default='stdout',
        help="Set output file with extension. Output format is JSON")
    parser.add_argument(
        "-i", "--input_file", default="files.txt",
        help="File with list of all files to search through.")

    # parser.add_argument(
    #     "-o", "--out", default='',
    #     help="Set output file, stdout by default")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    gus = Get_unique_symbols(
        files=args.files,
        exts=args.extensions,
        folders=args.folders,
        database=args.database,
        input_file=args.input_file)
    # dirs=args.directories,
    # exts=args.extensions)

    gus.finalize(args.output)
    # gus.print_symbols(args.out)

    end = time.time()
    print(f'Total time: {end - start}')

if __name__ == "__main__":
    main()
