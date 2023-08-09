#!/usr/bin/python3.8
"""Analyze semantic labels and musescore xml files and export to csv pandas file.

Works with:
    - generated semantic labels
        - works only on ORIGINAL SEMANTIC ENCODING, not any of shortened version

Analyzed properties:
    - polyphonic score (Yes or No)
    - note and rest count for measure
    - note and rest count for stave
    - etc (see column names)

Usage:
$ python3 musescore_analyzer.py -i labels.semantic -o mscz_analyzer_stats.csv
Generates statistics for labels in labels.semantic file to file mscz_analyzer_stats.csv

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
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

# Import local library, download from https://github.com/vlachvojta/polyphonic-omr-by-sachindae
sys.path.append(os.path.join(rel_dir, '..', '..', 'lib', 'polyphonic-omr-by-sachindae', 'reverse_converter'))
from semantic_to_music21 import parse_semantic_to_measures
print(sys.path)

class LabelAnalyzer:
    """Analyze semantic labels and musescore xml files and export to csv pandas file."""

    EMPTY_SYSTEM_ID = 'EMPTY_SYSTEM_ID'

    def __init__(self, label_files: str,
                 output_file: str = 'stats.csv',
                 high_dens_threshold_min: float = 41.0,
                 high_dens_threshold_max: float = None,
                 verbose: bool = False):
                 # musicxml_files: str, input_folders: str, file_extensions_for_input_folders: list,
        self.label_files = label_files if label_files else []
        self.output_file = output_file if output_file.endswith('csv') else f'{output_file}.csv'
        self.high_dens_threshold_min = high_dens_threshold_min
        self.high_dens_threshold_max = high_dens_threshold_max
        self.verbose = verbose
        # self.musicxml_files = musicxml_files if musicxml_files else []
        # self.input_folders = input_folders if input_folders else []
        # self.file_extensions_for_input_folders = file_extensions_for_input_folders

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO,format='[%(levelname)-s]\t- %(message)s')

        # Load labels
        logging.info(f'Loading labels from {len(self.label_files)} files.')
        self.labels = {}
        for label_file in self.label_files:
            self.labels.update(LabelAnalyzer.load_labels(label_file))
        if not self.labels:
            logging.info('No valid semantic LABELS in given folders and files.')
        else:
            logging.info(f'\tFound {len(self.labels)} labels.')

        # Create output directory if needed
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def __call__(self):
        if not self.labels:
            logging.error("No images or labels where found, cannot generate stats.")
            return

        # df = pd.DataFrame(self.labels.keys(), dtype=pd.str, columns=['system_id'])
        df = pd.DataFrame.from_dict(self.labels, orient='index', columns=['labels'])
        df.index = df.index.set_names(['system_id'])

        for new_column in ['type']:
            df['type'] = 'semantic_labels'
            df['type'] = df['type'].astype('category')

        # print(df.count(axis='columns')[0])  # get the number of columns

        # df.insert(df.count(axis='columns')[0], 'is_polyphonic', np.nan)
        new_columns = ['is_polyphonic', 'char_length', 'symbol_count', 'measure_count',
                       'notes_count', 'rests_count', 'max_symbols_in_measure', 'density', 
                       'min_voices', 'mean_voices', 'max_voices']
        for new_column in new_columns:
            df[new_column] = np.nan
            df[new_column] = df[new_column].astype('category')

        df['voices'] = np.nan

        # df = df.iloc[:20]
        df = df.apply(self.get_stats_for_row, axis=1)

        print('------------------------------- STATS: -------------------------------')
        for column in new_columns:
            if not column in df:
                print(f'col: {column} not in df')
                continue

            print(f'Col: {column} values. min: {df[column].min()}, '
                  f'mean: {df[column].mean():.2f}, max: {df[column].max()}')

        voices_flat = [item for sublist in df['voices'] for item in sublist]
        print(f'Col: voices_flat. values. min: {min(voices_flat)}, '
                f'mean: {np.mean(voices_flat):.2f}, max: {max(voices_flat)}')

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

        self.save_polyphonic_indexes(df)
        self.save_high_density_indexes(df)

    def save_polyphonic_indexes(self, df: pd.DataFrame) -> None:
        """Get polyphonic staff_ids and save to new file."""
        poly_staves = df[(df['is_polyphonic'])].index.tolist()
        output_file_poly = f'{self.output_file}_polyphonic_staves.txt'

        print(f'Found {len(poly_staves)} polyphonic staves. Saving to {output_file_poly}')
        Common.write_to_file('\n'.join(sorted(poly_staves)), output_file_poly)

    def save_high_density_indexes(self, df: pd.DataFrame) -> None:
        """Get big density subset and save system ids to new file."""
        if self.high_dens_threshold_max:
            high_density_subset = df[
                (df['density'] >= self.high_dens_threshold_min) &
                (df['density'] < self.high_dens_threshold_max)]
            density = f'{int(self.high_dens_threshold_min)}_to_{int(self.high_dens_threshold_max)}'
        else:
            high_density_subset = df[df['density'] >= self.high_dens_threshold_min]
            density = f'{int(self.high_dens_threshold_min)}'

        high_density_subset.to_csv('high_density_subset.csv')

        len_of_high_density = len(high_density_subset)
        output_file_staves = f'{self.output_file}_high_density_staves_{density}.txt'
        output_file_parts = f'{self.output_file}_high_density_parts_{density}.txt'
        output_file_mscz = f'{self.output_file}_high_density_mscz_{density}.txt'

        print(f'Found {len_of_high_density} staves with density bigger or equal to {density}. '
              f'Saving to {output_file_staves}')
        staves = high_density_subset.index.tolist()
        Common.write_to_file('\n'.join(staves), output_file_staves)

        # Get unique parts and mscz file names
        parts = set()
        msczs = set()
        for stave_id in staves:
            mscz, part, *_ = re.split(r'_', stave_id)
            msczs.add(mscz)
            parts.add(f'{mscz}_{part}')

        Common.write_to_file('\n'.join(sorted(parts)), output_file_parts)
        Common.write_to_file('\n'.join(sorted(msczs)), output_file_mscz)

    def get_stats_for_row(self, row: pd.Series) -> pd.Series:
        """Gets all stats needed for row from DataFrame."""
        logging.debug('--------------- new label_sequence')
        label_sequence = row['labels']
        logging.debug(f'{row.name}: {label_sequence[:150]}')
        row['char_length'] = len(label_sequence)

        row['is_polyphonic'] = self.is_sequence_polyphonic(label_sequence)

        # print(f'seq: {label_sequence}')
        # splitted = re.split(r'\s+', label_sequence)
        # print(f"split to symbols: {splitted}")
        # len_ = len(re.split(r'\s+', label_sequence)) - 1
        # print(f"len: {len_}")
        # Get number of musical symbols
        row['symbol_count'] = len(re.split(r'\s+', label_sequence)) - 1

        # Get number of measures
        potential_measures = re.split(r'barline|\|', label_sequence)
        row['measure_count'] = len(list(filter(None, potential_measures)))

        # Get number of notes and gracenotes
        row['notes_count'] = len(re.findall(r'note-[a-gA-G]\S+\s', label_sequence))

        # Get number of rests
        row['rests_count'] = len(re.findall(r'rest-\S+\s', label_sequence))

        row['max_symbols_in_measure'] = self.get_max_symbols_in_measure(label_sequence)

        row['density'] = row['symbol_count'] / row['measure_count']

        row['voices'] = self.get_voices(label_sequence)
        voices = self.get_voices(label_sequence)
        row['min_voices'] = min(voices)
        row['mean_voices'] = np.mean(voices)
        row['max_voices'] = max(voices)

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

    def get_voices(self, sequence: str) -> list:
        """Get label sequence as a string, count number of ACTUAL VOICES, chord is one voice here."""
        measures = parse_semantic_to_measures(sequence)

        voice_counts = []
        for measure in measures:
            max_voices_in_measure = max([symbol_group.get_voice_count() for symbol_group in measure.symbol_groups])
            voice_counts.append(max_voices_in_measure)

        return voice_counts

    def get_voices_old(self, sequence: str) -> list:
        """Get label sequence as a string, count length of symbols in EVERY CHORD.

        Return in a list."""
        # print(f'in: {sequence}')

        chords = re.split(r'\s+\+\s+', sequence)
        # print(f'chords: {chords}')

        return [len(re.split(r'\s+', chord)) for chord in chords]

    @staticmethod
    def load_labels(filename: str) -> dict:
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
            system_id, sequence = LabelAnalyzer.parse_label_line(label_line)
            if system_id and sequence:
                if system_id == LabelAnalyzer.EMPTY_SYSTEM_ID:
                    labels_dict[filename] = sequence
                else:
                    labels_dict[system_id] = sequence

        return labels_dict

    @staticmethod
    def parse_label_line(label_line) -> (str, str):
        """Parse a label line. Return tuple of two strings (system id and sequence of labels).

        Label line consists of label header and sequence of labels.
        Label header consists of system_id and sometimes other data not relevant to this script.
        """
        if not label_line:
            return '', ''

        line_splitted = re.split(r'"', label_line)

        if len(line_splitted) == 1:
            return LabelAnalyzer.EMPTY_SYSTEM_ID, label_line

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
        "-o", "--output-file", type=str, default='mscz_analyzer_stats.csv.csv',
        help="Output file to export pandas csv to.")
    parser.add_argument(
        "-t", "--high-dens-threshold-min", type=float, default=41.0,
        help="Minimal threshold for measure density of labels to export to a separate file.")
    parser.add_argument(
        "-T", "--high-dens-threshold-max", type=float, default=None,
        help="Maximal threshold for measure density of labels to export to a separate file.")
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
    # parser.add_argument(
    #     "-m", "--musicxml-files", type=str, nargs='*',
    #     help="Input files to load musescore xml.")
    # parser.add_argument(
    #     "-i", "--input-folders", type=str, nargs='*',
    #     help=("Input folders to load labels or musescore xml from. "
    #           "(use with --file-extensions-for-input-folders for better results)"))
    # parser.add_argument(
    #     "-e", "--file-extensions-for-input-folders", nargs='*', default=['semantic', 'musicxml'],
    #     help=("Set file extensions for files in given input folders. " +
    #           "Use in combination with --input-folders."))
    return parser.parse_args()

def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    analyzer = LabelAnalyzer(
        label_files=args.label_files,
        output_file=args.output_file,
        high_dens_threshold_min=args.high_dens_threshold_min,
        high_dens_threshold_max=args.high_dens_threshold_max,
        verbose=args.verbose)
        # musicxml_files=args.musicxml_files,
        # input_folders=args.input_folders,
        # file_extensions_for_input_folders=args.file_extensions_for_input_folders,
    analyzer()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
