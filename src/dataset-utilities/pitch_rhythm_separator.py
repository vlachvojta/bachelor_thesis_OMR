#!/usr/bin/python3.8
"""Simple script for separating rythm and pitch aspect of symbols.

Pitch: note-HEIGHT, gracenote-HEIGHT
Rhythm: note_LENGTH, gracenote_LENGTH and the rest of symbols

Used for evaluation of model outputs.

SUPPORTED ENCODING:
- plain semantic encoding from PrIMus dataset
- pseudo-semantic encoding generated from musescore files by gen_labels.py in https://github.com/vlachvojta/polyphonic-omr-by-sachindae.git
- One spacific translation of pseudo-semantic encoding to shorter version
"""

import argparse
import re
import os
import time
# import sys

from common import Common


class PRSeparator:
    """Simple module for separating rythm and pitch aspect of symbols. 

    Used for evaluation of model outputs.
    """

    def __init__(self, input_folder: str = '.', file_extension: str = None,
                 input_mode: str = 'raw', output_folder: str = '.'):
        self.input_folder = input_folder
        self.file_extension = file_extension
        self.input_mode = input_mode
        self.output_folder = output_folder

        print(f'Trying to load files from {self.input_folder} with extension {self.file_extension}')
        # Load input file names
        self.input_files = Common.listdir(self.input_folder, [self.file_extension])
        print(f'Loaded {len(self.input_files)} input file(s).')

        # Create output part if necessary
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def __call__(self):
        if not self.input_files:
            raise ValueError('NO input files found.')

        # Go through input files
        for file in self.input_files:
            print(f'Working file {file}')

            lines = re.split(r'\n', Common.read_file(file))
            print(f'File has {len(lines)} lines.')

            # On every line separate rhythm and pitch aspect
            pitch_lines = []
            rhythm_lines = []
            for line in lines:
                if not line:
                    continue
                pitch, rhythm = self.separate_line(line)
                pitch_lines.append(pitch)
                rhythm_lines.append(rhythm)

            # Save to two output files
            output_file = os.path.join(self.output_folder, os.path.basename(file))
            output_file_pitch = f'{output_file}.pitch'
            output_file_rhythm = f'{output_file}.rhythm'

            Common.write_to_file('\n'.join(pitch_lines), output_file_pitch)
            Common.write_to_file('\n'.join(rhythm_lines), output_file_rhythm)


    def separate_line(self, line: str) -> (str, str):
        """Separate line of labels to pitch and rhythm.

        Return two strings. Pitch symbols and rhythm symbols IN THIS ORDER."""
        if self.input_mode == 'raw':
            pitches, rhythms = PRSeparator.separate_labels(line)
            # labels = re.split(r'\s+', line)
            out_pitches = ' '.join(pitches)
            out_rhythms = ' '.join(rhythms)
        elif self.input_mode == 'pero':
            head, body, _ = re.split(r'\"', line)

            pitches, rhythms = PRSeparator.separate_labels(body)

            out_pitches = f"{head}\"{pitches}\""
            out_rhythms = f"{head}\"{rhythms}\""

        # print(out_pitches)
        # print(out_rhythms)

        return out_pitches, out_rhythms

    @staticmethod
    def separate_labels(labels: str = '') -> (str, str):
        """Get clean line of labels as a string, divide into into pitch and rhythm symbols

        Pitch: note-HEIGHT, gracenote-HEIGHT
        Rhythm: note_LENGTH, gracenote_LENGTH and the rest of symbols

        Return str lines of PITCH and RHYTHM IN THIS OREDER."""
        rhythms = []
        pitches = []

        labels = re.split(r'\s+', labels)

        for label in labels:
            # Check for Semantic labels
            if label.startswith('note') or label.startswith('gracenote'):
                note, pitch, *rest = re.split(r'-|_', label)
                pitches.append(f'{note}-{pitch}')
                rhythms.append(f"{note}-{'_'.join(rest)}")
                continue

            # Check for specific type of shortened semantic-like encoding
            match = re.match(r'[A-Ga-g](N|#+|b+)?\d', label)
            if match:
                pitches.append(match.group(0))
                match_len = len(match.group(0))
                rhythms.append(f'N{label[match_len:]}')
                continue

            rhythms.append(label)

        return ' '.join(pitches), ' '.join(rhythms)


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-folder", type=str, default='.',
        help="Folder to read all files from. USE WITH EXTENSION")
    parser.add_argument(
        "-e", "--file-extension", type=str, default=None,
        help="File extesions to look for in input folder.")
    parser.add_argument(
        "-m", "--input-mode", default='raw', choices=['raw', 'pero'],
        help="Input mode of parsing begging of a file")
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
        file_extension=args.file_extension,
        input_mode=args.input_mode,
        output_folder=args.output_folder)
    separator()

    end = time.time()
    print(f'Total time: {end - start}')


if __name__ == "__main__":
    main()
