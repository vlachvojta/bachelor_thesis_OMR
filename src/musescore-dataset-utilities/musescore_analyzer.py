#!/usr/bin/python3.8
"""Analyze semantic labels and musescore xml files and export to csv pandas file.

Works with:
    - generated semantic labels (implementation in process)
        - works only on ORIGINAL SEMANTIC ENCODING, not any of shortened version
    - musicxml separated parts (TBD)
    - raw musicxml files exported from musescore (TBD)

Analyzed properties:
    - polyphonic score (Yes or No)
    - note and rest count for measure
    - note and rest count for stave

Usage:
$ python3 musescore_analyzer.py -i labels.semantic -o mscz_analyzer_stats.csv
Generates statistics for labels in labels.semantic file to file mscz_analyzer_stats.csv
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
                 file_extensions_for_input_folders: list, output_file: str = 'mscz_analyzer_stats.csv.csv',
                 verbose: bool = False):
        self.label_files = label_files if label_files else []
        self.musicxml_files = musicxml_files if musicxml_files else []
        self.input_folders = input_folders if input_folders else []
        self.file_extensions_for_input_folders = file_extensions_for_input_folders
        self.output_file = output_file if output_file.endswith('.csv') else f'{output_file}.csv'
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
            logging.info('No valid semantic LABELS in given folders and files.')
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

        # print(df.count(axis='columns')[0])  # get the number of columns

        # df.insert(df.count(axis='columns')[0], 'is_polyphonic', np.nan)
        new_columns = ['is_polyphonic', 'char_length', 'symbol_count', 'measure_count',
                       'notes_count', 'rests_count', 'max_symbols_in_measure']
        for new_column in new_columns:
            df[new_column] = np.nan
            df[new_column] = df[new_column].astype('category')

        # df = df.iloc[:20]   # TODO delete this, only for development purposes
        df = df.apply(self.get_stats_for_row, axis=1)

        ## Inplace sort by measure_count descending order
        # df.sort_values("symbol_count", inplace = True, ascending = False)

        print('------------------------------- RESULTS: -------------------------------')
        print(df.info())
        print('------------------------------------------------------------------------')
        print(df)
        print('------------------------------------------------------------------------')

        # df['xxx'].plot(kind='hist', bins=10)
        
        df.to_csv(self.output_file)
        print(f'Dataframe saved to {self.output_file}')

    def get_stats_for_row(self, row: pd.Series) -> pd.Series:
        """Gets all stats needed for row from DataFrame."""
        label_sequence = row['labels']
        logging.debug(label_sequence[:150])
        row['char_length'] = len(label_sequence)

        row['is_polyphonic'] = self.is_sequence_polyphonic(label_sequence)

        # Get number of musical symbols
        row['symbol_count'] = len(re.split(r'\s+', label_sequence)) - 1

        # Get number of measures
        potential_measures = re.split(r'barline', label_sequence)
        row['measure_count'] = len(list(filter(None, potential_measures)))

        # Get number of notes and gracenotes
        row['notes_count'] = len(re.findall(r'note-[a-gA-G]\S+\s', label_sequence))

        # Get number of rests
        row['rests_count'] = len(re.findall(r'rest-\S+\s', label_sequence))

        row['max_symbols_in_measure'] = self.get_max_symbols_in_measure(label_sequence)
        logging.debug('---------------')

        return row

    def get_max_symbols_in_measure(self, label_sequence) -> int:
        """Split sequence to measures and return maximum symbols in one measure."""
        measures = re.split(r'barline', label_sequence)

        symbol_counts = []

        for measure in measures:
            if len(measure) < 2:
                continue

            symbols = re.split(r'\s+', measure)
            symbols = list(filter(None, symbols))
            symbols_count = len(symbols)

            pluses = re.findall(r'\+', measure)
            plus_count = len(pluses)
            symbol_counts.append(symbols_count - plus_count)

        return max(symbol_counts)

    def is_sequence_polyphonic(self, sequence: str) -> bool:
        """Returns True if sequence of labels is polyphonic. False otherwise."""
        if not '+' in sequence:
            return False

        sequence_splitted = re.split(r'\+', sequence)

        for potential_chord in sequence_splitted:
            potential_chord_splitted = re.split(r'\s+', potential_chord)
            potential_chord_splitted_len = len(list(filter(None, potential_chord_splitted)))

            if potential_chord_splitted_len > 1:
                return True

        return False

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
        system_id, *_ = re.split(r'\s', label_header)

        if not rest:
            logging.warning(f'Sequence {system_id} is EMPTY. Skipping.')
            return '', ''

        if len(rest) == 0:
            logging.warning(f'Label line {system_id} has wrong format. '
                            'Returning the whole line.')
            return system_id, label_line

        if len(rest) == 1 or len(rest) == 2:
            return system_id, rest[0]

        if len(rest) > 2:
            # Sequence has bad format, find first non-empty sequence and work only with it

            sub_sequence_lens = []
            for sub_sequence in rest:
                sub_sequence_lens.append(len(sub_sequence))

            longest_sub_sequence_len = max(sub_sequence_lens)
            longest_sub_sequence_i = sub_sequence_lens.index(longest_sub_sequence_len)

            if longest_sub_sequence_len > 0:
                logging.warning(f'Label line {system_id} has too many seperators (") in it. '
                                f'Using only the {longest_sub_sequence_i + 1}. element '
                                f'(len: {longest_sub_sequence_len}).')
                return system_id, rest[longest_sub_sequence_i]

            logging.warning(f'Label line {system_id} has wrong format. '
                            'Returning the whole line after system_id.')
            return system_id, rest

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
        "-o", "--output-file", type=str, default='mscz_analyzer_stats.csv.csv',
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
