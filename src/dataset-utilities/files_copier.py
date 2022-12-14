#!/usr/bin/python3.8

import argparse
import re
import sys
import os
from common import Common
import time


class Files_copier:

    file_names = []
    file_groups = []
    file_translator = {}
    exts = []
    output = ''

    def __init__(self, exts: list = ['semantic', 'png'], folders: list = ['.'],
                 output: str = 'output_folder',
                 copy_names: bool = False) -> None:
        print('Hello from FILES_COPIER')
        self.output = output
        self.exts = exts

        if not os.path.exists(output):
            os.mkdir(output)

        files = []
        for folder in folders:
            files += Common.get_files(folder, exts)

        files = list(set(files))
        self.file_names = Common.check_existing_files(files)

        print(f'Found {len(self.file_names)} files with one of '
              f'{len(exts)} extensions.')

        self.file_groups = Common.get_complete_group_names(self.file_names,
                                                           exts)

        print(f'Found {len(self.file_groups)} complete file groups ')
        diff = len(self.file_names) - (len(self.file_groups) * len(exts))
        if diff:
            print(f'{diff} files are in incomplete group.')
        print(f'(every dot is 1000 parsed files.)')

        for i, file_group in enumerate(self.file_groups):
            self.write_group(file_group, i)
            self.file_translator.update({f'{i:06}': file_group})
            if i % 1000 == 0:
                print('.', end='')
                sys.stdout.flush()
        print('')

        Common.save_dict_as_json(self.file_translator,
                                 os.path.join(output, '0_file_translator.json'))

        # total_symbols = Common.sum_lists_in_dict(self.unique_symbols)
        # new_symbols_count = total_symbols - loaded_symbols_sum
        # print(f'{new_symbols_count} new symbols discovered. '
        #       f'({total_symbols} total)')

    def write_group(self, file_group: str = '', i: int = 0) -> None:
        ...
        # for ext in self.exts:
            # read file from: file_group + ext
            # write it to: self.output + i + ext (os.path.join nebo něco)
            # self.read_write_file(file_group + ext, i + ext)


def parseargs():
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-f", "--files", nargs='*', default=[],
    #     help=("Files to read symbols from, you can add more files\n" +
    #           "or use bash regex expr.\n" +
    #           "USE FULL FILE PATH (relative or absolute)"))
    parser.add_argument(
        "-e", "--extensions", nargs='*', default=['semantic', 'png'],
        help=("Set file extensions for files in given folder\n" +
              "Use in combination with --directories."))
    parser.add_argument(
        "-F", "--src_folders", nargs='*', default=['.'],
        help=("Directories where to look for files with given extensions. \n" +
              "Use in combination with --extensions."))
    parser.add_argument(
        "-o", "--output_folder", default='output_folder',
        help="Set output file with extension. Output format is JSON")
    parser.add_argument(
        "-c", "--copy_names", action="store_true", default='False',
        help="Set output file with extension. Output format is JSON")
    # parser.add_argument(
    #     "-i", "--input_file", default="files.txt",
    #     help="File with list of all files to search through.")
    # parser.add_argument(
    #     "-o", "--out", default='',
    #     help="Set output file, stdout by default")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    # fc = Files_copier(
    Files_copier(
        exts=args.extensions,
        folders=args.src_folders,
        output=args.output_folder,
        copy_names=args.copy_names)
    # database=args.database,
    # dirs=args.directories,
    # exts=args.extensions)

    # gus.finalize(args.output)
    # gus.print_symbols(args.out)

    end = time.time()
    print(f'Total time: {end - start}')


if __name__ == "__main__":
    main()
