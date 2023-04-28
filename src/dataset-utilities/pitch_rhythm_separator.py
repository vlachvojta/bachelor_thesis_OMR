#!/usr/bin/python3.8
"""Simple script for separating rythm and pitch aspect of symbols. 

Used for evaluation of model outputs.

!!! WORKS ONLY ON SEMANTIC ENCODING SO FAR. !!!
"""

import argparse
import re
import sys
import time

from common import Common


class PRSeparator:
    """Simple module for separating rythm and pitch aspect of symbols. 

    Used for evaluation of model outputs.
    """

    def __init__(self, input_folder: str, file_extensions: list,
                 output_folder: str):
        self.input_folder = input_folder
        self.file_extensions = file_extensions
        self.output_folder = output_folder

        # TODO Load input file names

    def __call__(self):
        ...
        # TODO go through files
        # On every line separate rhythm and pitch aspect
        # Save to two output files


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-folder", type=str,
        help="Folder to read all files from. USE WITH EXTENSION")
    parser.add_argument(
        "-e", "--file-extensions", nargs='+',
        help="File extesions to look for in input folder.")
    parser.add_argument(
        "-o", "--output-folder", default='.',
        help="Set output folder.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    separator = PRSeparator(
        input_folder=args.input_folder,
        file_extensions=args.file_extensions,
        output_folder=args.output_folder)
    separator()

    end = time.time()
    print(f'Total time: {end - start}')


if __name__ == "__main__":
    main()
