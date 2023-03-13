#!/usr/bin/python3.8
"""Split score from lines to pages.

Load .musicxml and corresponding .mscx files and add page breaks to the.mscx file
accoring to the "new-system" tags in .musicxml.

Usage:
$ python3 page_breakinator.py -i 100.musicxml -i 100.mscx
resulting in creating files 100_b.mscx
"""

import argparse
# import re
import sys
import os
import time
from copy import deepcopy

from lxml import etree

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class PageBreakinator:
    """Split score from lines to pages."""
    def __init__(self, input_files: list,
                 output_folder: str = '.'):
        self.output_folder = output_folder

        self.input_files = Common.check_existing_files(input_files)
        self.input_files = Common.check_files_extention(self.input_files, ['musicxml', 'mscx'])
        if not self.input_files:
            raise ValueError('No valid input files provided.')

        print(f'Found {len(self.input_files)} input files.')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def __call__(self):
        for file_in in self.input_files:
            print(f'Working with: {file_in}')
            file_type = file_in.split('.')[-1]

        print('--------------------')
        print('Results:')
        print(f'From {len(self.input_files)} input files.')


def parseargs():
    """Parse arguments."""
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-files", nargs='+',
        help="Input XML files to process.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='.',
        help="Output folder to write files to.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    breakinator = PageBreakinator(
        input_files=args.input_files,
        output_folder=args.output_folder)
    breakinator()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
