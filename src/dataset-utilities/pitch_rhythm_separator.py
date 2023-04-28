#!/usr/bin/python3.8
"""Simple script for separating rythm and pitch aspect of symbols. 

Used for evaluation of model outputs.

!!! WORKS ONLY ON SEMANTIC ENCODING SO FAR. !!!
"""

import argparse
import re
import os
import sys
import time

from common import Common


class PRSeparator:
    """Simple module for separating rythm and pitch aspect of symbols. 

    Used for evaluation of model outputs.
    """

    def __init__(self, input_folder: str = '.', file_extension: str = 'semantic',
                 input_mode: str = 'raw', output_folder: str = '.'):
        self.input_folder = input_folder
        self.file_extension = file_extension
        self.input_mode = input_mode
        self.output_folder = output_folder

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
                pitch, rhythm = self.separate(line)
                pitch_lines.append(pitch)
                rhythm_lines.append(rhythm)

            # Save to two output files
            output_file = os.path.join(self.output_folder, os.path.basename(file))
            output_file_pitch = f'{output_file}.pitch'
            output_file_rhythm = f'{output_file}.rhythm'

            Common.write_to_file('\n'.join(pitch_lines), output_file_pitch)
            Common.write_to_file('\n'.join(rhythm_lines), output_file_rhythm)


    def separate(self, line: str) -> (str, str):
        """Separate line of labels to pitch and rhythm.

        Return two strings. Pitch symbols and rhythm symbols IN THIS ORDER."""
        rhythms = []
        pitches = []

        if self.input_mode == 'raw':
            labels = re.split(r'\s+', line)
        elif self.input_mode == 'pero':
            head, body, _ = re.split(r'\"', line)
            labels = re.split(r'\s+', body)

        print(f'Loaded {len(labels)} labels on this line.')

        for label in labels:
            if label.startswith('note') or label.startswith('gracenote'):
                note, pitch, *rest = re.split(r'-|_', label)
                pitches.append(f'{note}-{pitch}')
                rhythms.append(f"{note}-{'_'.join(rest)}")
                # print(f'pitch: {note}-{pitch}')
                # print(f'rhythm: {note}-{"_".join(rest)}')
            else:
                rhythms.append(label)

        if self.input_mode == 'raw':
            out_pitches = ' '.join(pitches)
            out_rhythms = ' '.join(rhythms)
        elif self.input_mode == 'pero':
            out_pitches = f"{head}\"{' '.join(pitches)}\""
            out_rhythms = f"{head}\"{' '.join(rhythms)}\""
        # print(out_pitches)
        # print(out_rhythms)

        return out_pitches, out_rhythms

# """"note-Gb6_half": "Gb6H", "note-Gb6_half.": "Gb6H.", "note-Gb6_quarter": "Gb6q", 
# "note-Gb6_quarter.": "Gb6q.", "note-Gb6_sixteenth": "Gb6S", 
# "note-Gb6_sixteenth.": "Gb6S.", "note-Gb6_sixty_fourth": "Gb6s", 
# "note-Gb6_sixty_fourth.": "Gb6s.", "note-Gb6_thirty_second": "Gb6T", 
# "note-Gb6_whole": "Gb6W", "note-Gb6_whole.": "Gb6W.", "note-Gb7_eighth": "Gb7z", 
# "note-Gb7_half": "Gb7H", "note-Gb7_hundred_twenty_eighth": "Gb7h", 
# "note-Gb7_quarter": "Gb7q", "note-Gb7_sixteenth": "Gb7S", "note-Gb7_sixty_fourth": "Gb7s", "note-Gb7_sixty_fourth.": "Gb7s.", "note-Gb7_thirty_second": "Gb7T", "note-Gbb2_eighth": "Gbb2z", "note-Gbb3_eighth": "Gbb3z", "note-Gbb3_half": "Gbb3H", "note-Gbb3_sixteenth": "Gbb3S", "note-Gbb4_half": "Gbb4H", "note-Gbb4_sixteenth": "Gbb4S", "note-Gbb5_eighth": "Gbb5z", "note-Gbb5_half": "Gbb5H", "note-Gbb5_sixteenth": "Gbb5S", "note-Gbb6_sixteenth": "Gbb6S", """"


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-folder", type=str, default='.',
        help="Folder to read all files from. USE WITH EXTENSION")
    parser.add_argument(
        "-e", "--file-extension", type=str, default='semantic',
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
