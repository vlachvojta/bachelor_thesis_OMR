#!/usr/bin/python3.8
"""Split multi-part music score files to multiple files with only one part per file.

File naming conventions: file.musicxml -> file_p[1-n].musixml 
    where n is the number of parts.

Example run:
$ python3 part_splitter.py -i 100.musicxml -o parts_out/
resulting in creating files parts_out/100_p00.musixml, parts_out/100_p01.musix etc.
"""

import argparse
# import re
import sys
import os
import time
from copy import deepcopy

from lxml import etree

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class PartSplitter:
    """Split multi-part music score files to multiple files with only one part per file."""
    def __init__(self, input_files: list,
                 output_folder: str = '.'):
        self.output_folder = output_folder

        self.input_files = Common.check_existing_files(input_files)
        self.input_files = Common.check_files_extention(self.input_files, 'musicxml')
        if not self.input_files:
            raise ValueError('No valid input files provided.')

        print(f'Found {len(self.input_files)} input files.')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def __call__(self):
        for file_in in self.input_files:
            print(f'Working with: {file_in}')
            xml_syntax_error_files = 0
            music_score_error_files = 0
            generated_files = 0

            try:
                file_tree = etree.parse(file_in)
            except etree.XMLSyntaxError:
                xml_syntax_error_files += 1
                continue

            # if not self.is_valid_music_score(file_tree):
            #     music_score_error_files += 1
            #     continue

            part_ids = self.get_valid_ids(file_tree)
            print(part_ids)

            new_trees = []
            for _ in range(len(part_ids)):
                new_trees.append(deepcopy(file_tree))

            for i, (part_id, new_tree) in enumerate(zip(sorted(part_ids), new_trees)):
                score_parts = new_tree.xpath('//score-part | //part')

                print(f'Found {len(score_parts)} score parts.')
                for part in score_parts:
                    if part.get('id') != part_id:
                        part.getparent().remove(part)

                print(len(new_tree.xpath(".//*")))

                file_out = file_in.split('.')[0]
                part_file_name = f'{file_out}_p{i:02d}.musicxml'
                part_path = os.path.join(self.output_folder, part_file_name)
                new_tree.write(part_path, pretty_print=True, encoding='utf-8', xml_declaration=True)
                generated_files += 1

        print('--------------------')
        print('Results:')
        print(f'From {len(self.input_files)} input files.')
        print(f'\t{xml_syntax_error_files} had xml syntax errors')
        print(f'\t{music_score_error_files} had music score errors')
        print(f'\t{generated_files} generated files')

    # def is_valid_music_score(self, tree: etree.Element) -> bool:
    #     """Check if the music score is valid."""

    #     # ? Some checks ?

    #     return True

    def get_params_of_tags(self, tree: etree.Element, tag: str, param: str) -> list:
        """Get the ids of the tags."""
        params = []
        for child in tree.xpath(f'//{tag}'):
            params.append(child.get(param))
        return params

    def get_valid_ids(self, tree)-> list:
        """Get only valid ids of parts in the tree."""
        score_part_ids = self.get_params_of_tags(tree, 'score-part', 'id')
        part_ids = self.get_params_of_tags(tree, 'part', 'id')
        return Common.intersection(score_part_ids, part_ids)


def parseargs():
    """Parse arguments."""
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-files", nargs='+',
        help="Input images to cut.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='.',
        help="Output folder to write cut imgs to.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    splitter = PartSplitter(
        input_files=args.input_files,
        output_folder=args.output_folder)
    splitter()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
