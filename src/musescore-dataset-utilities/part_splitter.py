#!/usr/bin/python3.8
"""Split multi-part music score files to multiple files with only one part per file.

File naming conventions: file.musicxml -> file_p[1-n].musixml 
    where n is the number of parts.

Example run:
$ python3 part_splitter.py -i 100.musicxml -o parts_out/
resulting in creating files parts_out/100_p1.musixml, parts_out/100_p2.musix etc.
"""

import argparse
# import re
import sys
import os
import time


rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class PartSplitter:
    """Split multi-part music score files to multiple files with only one part per file."""
    def __init__(self, input_files: list,
                 output_folder: str = '.'):
        self.output_folder = output_folder
        self.input_files = input_files

        self.input_files = Common.check_existing_files(input_files)
        if not self.input_files:
            raise ValueError('No valid input files provided.')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def __call__(self):
        for file in self.input_files:
            print(f'Working with: {file}')


def parseargs():
    """Parse arguments."""
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-files", nargs='+',
        help="Input images to cut.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='.',
        help="Output folder to write cut imgs to.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    splitter = PartSplitter(
        input_files=args.input_files,
        output_folder=args.output_folder)
    splitter()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
