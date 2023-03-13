#!/usr/bin/python3.8
"""Split score from lines to pages.

Load .musicxml and corresponding .mscx files and add page breaks to the.mscx file
accoring to the "new-system" tags in .musicxml.

Usage:
$ python3 page_breakinator.py -i 100.musicxml -i 100.mscx
resulting in creating files 100_b.mscx
"""

import argparse
# import re
import sys
import os
import time

from lxml import etree

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class PageBreakinator:
    """Split score from lines to pages."""
    def __init__(self, input_files: list,
                 output_folder: str = '.'):
        self.output_folder = output_folder

        self.input_files = Common.check_existing_files(input_files)
        self.input_files = self.get_valid_pairs(self.input_files)

        if not self.input_files:
            raise ValueError('No valid input files provided.')

        print(f'Found {len(self.input_files)} input file pairs.')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def __call__(self):
        xml_syntax_error_files = 0
        music_score_error_files = 0
        generated_files = 0

        page_break_str = '<LayoutBreak><subtype>page</subtype></LayoutBreak>'

        for file_in in self.input_files:
            print(f'Working with: {file_in}')

            file_music = file_in + '.musicxml'
            file_mscx = file_in + '.mscx'

            try:
                music_tree = etree.parse(file_music)
                mscx_tree = etree.parse(file_mscx)
            except etree.XMLSyntaxError:
                xml_syntax_error_pairs += 1
                continue

            # Count measures in both files
            music_measures = music_tree.xpath('//measure')
            mscx_measures = mscx_tree.xpath('//Measure')

            if len(music_measures) != len(mscx_measures):
                music_score_error_pairs += 1
                continue

            new_system_tags = 0
            for music_meassure, mscx_measure in zip(music_measures, mscx_measures):
                print_tag = music_meassure.xpath('./print/@new-system')
                if print_tag:
                    mscx_measure.append(etree.fromstring(page_break_str))
                    new_system_tags += 1

                    print(f'Found new-system tag: {print_tag[0]}')
                    # print(etree.tostring(print_tag[0]))

                    # for elem in music_meassure:
                    #     print(f'elem.tag: {elem.tag}, elem.text: {elem.text}')
                    # # print(music_meassure.children[0].tag)
            print(f'Found {new_system_tags} new-system tags.')

            file_out_path = os.path.join(self.output_folder, f'{file_in}_b.mscx')
            mscx_tree.write(file_out_path, pretty_print=True,
                           encoding='utf-8', xml_declaration=True)
            generated_files += 1


        print('--------------------')
        print('Results:')
        print(f'From {len(self.input_files)} input file pairs:')
        print(f'\t{xml_syntax_error_files} pairs had XML syntax errors')
        print(f'\t{music_score_error_files} pairs had music score errors')
        print(f'\t{generated_files} generated files')

    def get_valid_pairs(self, input_files: list) -> list:
        """Find pairs of files with valid .musicxml and .mscx extensions."""
        file_bases = [os.path.splitext(os.path.basename(file))[0]
                      for file in input_files]
        file_bases = list(set(file_bases))

        valid_pairs = []
        for file in file_bases:
            file_music = file + '.musicxml'
            file_mscx = file + '.mscx'

            if file_music in input_files and file_mscx in input_files:
                valid_pairs.append(file)

        return valid_pairs


def parseargs():
    """Parse arguments."""
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-files", nargs='+',
        help="Input XML files to process.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='.',
        help="Output folder to write files to.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    breakinator = PageBreakinator(
        input_files=args.input_files,
        output_folder=args.output_folder)
    breakinator()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
