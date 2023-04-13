#!/usr/bin/python3.8
"""Load label and image pairs with specific condition from pair folder.

Usage:
$ python3 copy_pairs.py -i 6_copied_pairs/big_density_systems.txt -o 6_copied_pairs_subset
Copies pairs of labels and images with name in input file to 6_copied_pairs_subset.
"""

import argparse
import re
import sys
import os
import time
import logging
# import numpy as np
# import pandas as pd
from musescore_analyzer import MusescoreAnalyzer

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class PairCopier:
    """Load label and image pairs with specific condition from pair folder."""

    EMPTY_SYSTEM_ID = 'EMPTY_SYSTEM_ID'

    def __init__(self, input_file: str, output_folder: str, verbose: bool = False):
        self.input_file = input_file
        self.output_folder = output_folder
        self.verbose = verbose

        dirname = os.path.dirname(input_file)
        self.image_folder = dirname if dirname else '.'
        self.label_file = os.path.join(dirname, '0_labels.semantic')

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO,format='[%(levelname)-s]\t- %(message)s')

        # Load list of images
        self.images = [img for img in os.listdir(self.image_folder) if img.endswith('.png')]
        print(f'Found {len(self.images)} images.')

        self.labels = MusescoreAnalyzer.load_labels(self.label_file)
        print(f'Found {len(self.labels)} labels.')

        self.system_ids = self.load_system_ids(self.input_file)
        print(f'Found {len(self.system_ids)} system IDs.')

    def __call__(self):
        ...
        # Analyze given labels

        # Select only labels with the condition

        # Copy selected labels and corresponding images to output folder

    def load_system_ids(self, input_file) -> list:
        """Get list of system IDs from input file.

        Get only first word in every line (ignore after first whitespace)"""
        file_lines = re.split(r'\n', Common.read_file(input_file))

        system_ids = []
        for line in file_lines:
            splitted = re.split(r'\s+', line)
            splitted = list(filter(None, splitted))
            if splitted:
                system_ids.append(splitted[0])

        return system_ids


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input_file", type=str, required=True,
        help="File with system_ids of pairs to copy.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='mscz_analyzer_stats.csv.csv',
        help="Output folder to copy selected pairs to.")
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
    return parser.parse_args()

def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    copier = PairCopier(
        input_file=args.input_file,
        output_folder=args.output_folder,
        verbose=args.verbose)
    copier()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
