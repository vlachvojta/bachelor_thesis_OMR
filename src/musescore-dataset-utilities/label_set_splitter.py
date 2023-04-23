#!/usr/bin/python3.8
"""Split labels dataset into two parts and IN RANDOM ORDER.

Used for training (trn) and testing(tst) of AI model.

Usage:
$ python3 labels_to_trn_and_tst.py -i labels.semantic -l 2000
Resulting in creating two files labels.semantic.tst and labels.semantic.trn,
    tst set having 2000 lines.
"""

import argparse
import sys
import os
import time
import random
import re

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class LabelSetSplitter:
    """Split labels dataset into two parts used for training (trn) and testing(tst)."""
    def __init__(self, input_file: str, output_file_name: str, tst_len: int = 2000):
        self.input_file = input_file
        self.tst_len = tst_len
        self.output_file_name = output_file_name

        self.labels = re.split(r'\n', Common.read_file(self.input_file))
        print(f'Found {len(self.labels)} labels.')

    def __call__(self):
        # Random shuffle labels
        labels_random = self.labels
        random.shuffle(labels_random)

        # Extract self.tst_len labels for tst set
        tst_subset = labels_random[:self.tst_len]
        trn_subset = labels_random[self.tst_len:]

        # Save both to corresponding file
        output = '\n'.join(tst_subset) + '\n'
        Common.write_to_file(output, f'{self.output_file_name}.tst')
        output = '\n'.join(trn_subset) + '\n'
        Common.write_to_file(output, f'{self.output_file_name}.trn')


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-file",
        help="Input file with all labels.")
    parser.add_argument(
        "-o", "--output-file-name",
        help="Output file name, script will add .tst and .trn at the end of each file.")
    parser.add_argument(
        "-l", "--tst-len", type=int, default=2000,
        help="Length of the tst subset.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    splitter = LabelSetSplitter(
        input_file=args.input_file,
        output_file_name=args.output_file_name,
        tst_len=args.tst_len)
    splitter()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
