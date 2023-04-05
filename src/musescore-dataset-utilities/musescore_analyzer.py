#!/usr/bin/python3.8
"""Analyze semantic labels and musescore xml files and export to csv pandas file.

Works with:
    - generated semantic labels (implementation in process)
    - musicxml separated parts (TBD)
    - raw musicxml files exported from musescore (TBD)

Analyzed properties:
    - polyphonic score (Yes or No)
    - note and rest count for measure
    - note and rest count for stave

Usage:
$ python3 musescore_analyzer.py -i labels.semantic -o stats.csv
Generates statistics for labels in labels.semantic file to file stats.csv
"""

import argparse
import re
import sys
import os
import time
import logging
import pandas as pd

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class MusescoreAnalyzer:
    """Analyze semantic labels and musescore xml files and export to csv pandas file."""
    def __init__(self, label_files: str, musicxml_files: str, input_folders: str,
                 file_extensions_for_input_folders: list, output_file: str = 'stats.csv',
                 verbose: bool = False):
        self.label_files = label_files
        self.musicxml_files = musicxml_files
        self.input_folders = input_folders
        self.file_extensions_for_input_folders = file_extensions_for_input_folders
        self.output_file = output_file
        self.verbose = verbose

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO,format='[%(levelname)-s]\t- %(message)s')

        # Load labels
        # print(f'Loading labels from {len(self.label_files)} files.')
        # self.labels = {}
        # for label_file in label_files:
        #     self.labels.update(self.load_labels(label_file))
        # if not self.labels:
        #     print('WARNING: No valid LABELS in given folder.')
        # else:
        #     print(f'\tFound {len(self.labels)} labels.')

        # Create output part if necessary
        # if not os.path.exists(self.output_folder):
        #     os.makedirs(self.output_folder)

        # self.no_new_system_parts = {}
        # self.not_fitting_staff_parts = {}
        # self.total_parts_found = set()
        # self.extra_label_parts = set()
        # self.extra_image_parts = set()
        # self.sum_values = 0

    def __call__(self):
        ...
        # if not self.images or not self.labels:
        #     print("ERROR: No images or labels where found, cannot generate no match.")
        #     return

        # images_base = [os.path.basename(image) for image in self.images]

        # image_parts = [self.get_part_name_with_suspicious(img) for img in images_base]
        # label_parts = [self.get_part_name(label) for label in self.labels]

        # image_parts = self.list_to_dict_sum(image_parts)
        # label_parts = self.list_to_dict_sum(label_parts)

        # print(f'LABELS originate from {len(label_parts)} parts.')
        # print(f'IMAGES originate from {len(label_parts)} parts.')

        # self.get_stats_about_parts(image_parts, label_parts)

        # sus_img_parts = self.get_sus_parts(images_base)  # - self.extra_image_parts
        # # print(f'\t{len(sus_img_parts)} part(s) has generated suspicious images.')
        # logging.debug(f'sus parts: {sus_img_parts}')

        # logging.debug('---- Finding complete parts: ----')
        # logging.debug('----(printing only incomplete)---')
        # complete_parts = self.get_complete_parts(image_parts, label_parts, sus_img_parts)

        # self.print_results(complete_parts, sus_img_parts)

        # self.copy_complete_parts(complete_parts)


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--label-files", type=str, nargs='*',
        help="Input files to load labels from.")
    parser.add_argument(
        "-m", "--musicxml-files", type=str, nargs='*',
        help="Input files to load musescore xml.")
    parser.add_argument(
        "-i", "--input-folders", type=str, nargs='*',
        help=("Input folders to load labels or musescore xml from. "
              "(use with --file-extensions-for-input-folders for better results)"))
    parser.add_argument(
        "-e", "--file-extensions-for-input-folders", nargs='*', default=['semantic', 'musicxml'],
        help=("Set file extensions for files in given input folders. " +
              "Use in combination with --input-folders."))
    parser.add_argument(
        "-o", "--output-file", type=str, default='stats.csv',
        help="Output file to export pandas csv to.")
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
    return parser.parse_args()

def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    analyzer = MusescoreAnalyzer(
        label_files=args.label_files,
        musicxml_files=args.musicxml_files,
        input_folders=args.input_folders,
        file_extensions_for_input_folders=args.file_extensions_for_input_folders,
        output_file=args.output_file,
        verbose=args.verbose)
    analyzer()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
