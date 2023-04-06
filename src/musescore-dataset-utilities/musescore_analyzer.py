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
import numpy as np
import pandas as pd

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class MusescoreAnalyzer:
    """Analyze semantic labels and musescore xml files and export to csv pandas file."""

    EMPTY_SYSTEM_ID = 'EMPTY_SYSTEM_ID'

    def __init__(self, label_files: str, musicxml_files: str, input_folders: str,
                 file_extensions_for_input_folders: list, output_file: str = 'stats.csv',
                 verbose: bool = False):
        self.label_files = label_files if label_files else []
        self.musicxml_files = musicxml_files if musicxml_files else []
        self.input_folders = input_folders if input_folders else []
        self.file_extensions_for_input_folders = file_extensions_for_input_folders
        self.output_file = output_file
        self.verbose = verbose

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO,format='[%(levelname)-s]\t- %(message)s')

        # Load labels
        logging.info(f'Loading labels from {len(self.label_files)} files.')
        self.labels = {}
        for label_file in self.label_files:
            self.labels.update(self.load_labels(label_file))
        if not self.labels:
            logging.info('No valid LABELS in given folders and files.')
        else:
            logging.info(f'\tFound {len(self.labels)} labels.')

        # TODO Load musicxml files

        # self.no_new_system_parts = {}
        # self.not_fitting_staff_parts = {}
        # self.total_parts_found = set()
        # self.extra_label_parts = set()
        # self.extra_image_parts = set()
        # self.sum_values = 0

    def __call__(self):
        if not self.labels:
            logging.error("No images or labels where found, cannot generate stats.")
            return

        # df = pd.DataFrame(self.labels.keys(), dtype=pd.str, columns=['system_id'])
        df = pd.DataFrame.from_dict(self.labels, orient='index', columns=['labels']
                                    )
        df.index = df.index.set_names(['system_id'])

        for new_column in ['type']:
            df['type'] = 'semantic_labels'
            df['type'] = df['type'].astype('category')

        print(df.count(axis='columns')[0])

        # df.insert(df.count(axis='columns')[0], 'is_polyphonic', np.nan)
        for new_column in ['is_polyphonic', 'char_length', 'symbol_length']:
            df[new_column] = np.nan
            df[new_column] = df[new_column].astype('category')

        df = df.iloc[:20]   # TODO delete this, only for development purposes
        df = df.apply(self.get_stats_for_row, axis=1)

        print(df.info())
        print('---------------------')
        print(df)


        # df['new_col'] = df.apply(self.get_stats, axis=1)

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

    def get_stats_for_row(self, row: pd.Series) -> pd.Series:
        """Gets different stats for row from DataFrame."""
        row['char_length'] = len(row['labels'])
        row['symbol_length'] = len(re.split(r'\s+', row['labels']))

        label_sequence = row['labels']

        if not '+' in label_sequence:
            row['is_polyphonic'] = False
        else:
            # print(label_sequence)
            chords_splitted = re.split(r'\+', label_sequence)
            # print(f'seq: {len(label_sequence)}, symbols: {len(chords_splitted)}')

        # row['is_polyphonic'] = self.is_sequence_polyphonic(row['labels'])

        return row

    def is_sequence_polyphonic(self, sequence: str) -> bool:
        """Returns True if sequence of labels is polyphonic. False otherwise."""
        return True

    def load_labels(self, filename: str) -> dict:
        """Load labels from one file and return as a dictionary."""
        if not os.path.isfile(filename):
            return {}

        data = Common.read_file(filename)

        if not data:
            return {}

        labels_list = re.split(r'\n', data)
        labels_list = list(filter(None, labels_list))  # filter out empty lines

        labels_dict = {}
        for label_line in labels_list:
            system_id, sequence = self.parse_label_line(label_line)
            if system_id and sequence:
                if system_id == self.EMPTY_SYSTEM_ID:
                    labels_dict[filename] = sequence
                else:
                    labels_dict[system_id] = sequence

        return labels_dict

    def parse_label_line(self, label_line) -> (str, str):
        """Parse a label line. Return tuple of two strings (system id and sequence of labels).

        Label line consists of label header and sequence of labels.
        Label header consists of system_id and sometimes other data not relevant to this script.
        """
        if not label_line:
            return '', ''

        line_splitted = re.split(r'"', label_line)

        if len(line_splitted) == 1:
            return self.EMPTY_SYSTEM_ID, label_line

        label_header, *rest = line_splitted
        rest = line_splitted[1:]
        system_id, *_ = re.split(r'\s', label_header)

        if not rest:
            logging.warning(f'Sequence {system_id} is EMPTY. Skipping.')
            return '', ''

        if len(rest) == 1 or len(rest) == 2:
            return system_id, rest[0]

        if len(rest) > 2:
            logging.warning(f'Sequence {system_id} has too many seperators (") in it. '
                            'Using only the first element.')
            return system_id, rest[0]

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
