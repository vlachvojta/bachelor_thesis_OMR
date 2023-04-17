#!/usr/bin/python3.8
"""Load label and image pairs given by input file.

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
from shutil import copyfile
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
        self.out_label_file = os.path.join(self.output_folder, '0_labels.semantic')

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

        # Create output part if necessary
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.copied_labels = {}

    def __call__(self):
        if not self.system_ids:
            logging.error('No system IDs to copy. Select a different file')

        success_files = 0
        fail_files = 0

        with open(self.out_label_file, 'w', encoding='utf-8') as out_label_file:
            for system_id in self.system_ids:
                if system_id in self.labels and system_id in self.labels:
                    self.copied_labels[system_id] = self.labels[system_id]

                    img_source = os.path.join(self.image_folder, system_id)
                    img_dest = os.path.join(self.output_folder, system_id)
                    logging.debug(f'Copying image ({img_source}) => ({img_dest})')
                    copyfile(img_source, img_dest)

                    label_seq = self.copied_labels[system_id]
                    out_label_file.write(
                        f'{system_id} {Common.PERO_LMDB_zero_tag} "{label_seq}"\n')

                    success_files += 1
                else:
                    print(f'NOT FOUND: {system_id}')
                    fail_files += 1

        print('')
        print('--------------------------------------')
        print('Results:')
        print(f'From {len(self.system_ids)} system_ids:')
        print(f'\t{success_files} copied successfully.')
        print(f'\t{fail_files} failed.')

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
        "-o", "--output-folder", type=str, required=True,
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
