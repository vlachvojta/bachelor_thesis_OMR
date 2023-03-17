#!/usr/bin/python3.8
"""Split multi-part music score files to multiple files with only one part per file.

Script also removes unwanted elements in remove_credits_and_stuff function.

Works for .musicxml and .mscx files (the ladder has not been tested in latest versions).
File naming conventions: file.musicxml -> file_p[1-n].musixml 
    where n is the number of parts.

Example run:
$ python3 part_splitter.py -i 100.musicxml -o parts_out/
resulting in creating files parts_out/100_p00.musicxml, parts_out/100_p01.musicxml etc.
"""

import argparse
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
    def __init__(self, input_files: list = None,
                 input_folder: str = None, output_folder: str = 'out'):
        self.output_folder = output_folder
        self.input_folder = input_folder

        if not input_folder is None:
            listdir = os.listdir(input_folder)
            if not input_files:
                input_files = [os.path.join(input_folder, file) for file in listdir]
            else:
                input_files = input_files + [os.path.join(input_folder, file) for file in listdir]

        if input_files is None:
            input_files = []
            print('No valid input files provided.')

        self.input_files = self.check_files(input_files)

        if not self.input_files:
            print('No valid input files provided.')

        print(f'Found {len(self.input_files)} input files.')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.xml_syntax_error_files = 0
        self.music_score_error_files = 0
        self.generated_files = 0

    def __call__(self):
        print(f'Going through {len(self.input_files)} files. (every dot is 200 files)')

        for i, file_in in enumerate(self.input_files):
            Common.print_dots(i, 200, 8_000)
            file_type = file_in.split('.')[-1]

            try:
                file_tree = etree.parse(file_in)
            except etree.XMLSyntaxError:
                self.xml_syntax_error_files += 1
                continue

            part_ids = self.get_valid_ids(file_tree, file_type)
            if not part_ids:
                self.music_score_error_files += 1
                continue

            file_tree = self.remove_credits_and_stuff(file_tree)

            new_trees = []
            for _ in range(len(part_ids)):
                new_trees.append(deepcopy(file_tree))

            for i, (part_id, new_tree) in enumerate(zip(sorted(part_ids), new_trees)):
                if file_type == 'musicxml':
                    score_parts = new_tree.xpath('//score-part | //part')
                    # print(f'Found {len(score_parts)} score parts.')

                    # Remove "part-groups" tags
                    for part_group in new_tree.xpath('//part-group'):
                        part_group.getparent().remove(part_group)

                    # Remove all other parts
                    for part in score_parts:
                        if part.get('id') != part_id:
                            part.getparent().remove(part)
                elif file_type == 'mscx':
                    parts = new_tree.xpath('//Part')
                    staffs = new_tree.xpath('/museScore/Staff')
                    # print(f'Found {len(parts)} parts and {len(staffs)} staffs.')

                    for part, staff in zip(parts, staffs):
                        staff_id = staff.get('id')

                        if staff_id != part_id:
                            staff.getparent().remove(staff)
                            part.getparent().remove(part)
                        else:
                            staff.set('id', str(1))

                file_out = os.path.basename(file_in).split('.')[0]
                part_file_name = f'{file_out}_p{i:02d}.{file_type}'
                part_path = os.path.join(self.output_folder, part_file_name)
                new_tree.write(part_path, pretty_print=True, encoding='utf-8')
                self.generated_files += 1

        self.print_results()

    def print_results(self):
        print('')
        print('--------------------')
        print('Results:')
        print(f'From {len(self.input_files)} input files:')
        print(f'\t{self.xml_syntax_error_files} had xml syntax errors')
        print(f'\t{self.music_score_error_files} had music score errors')
        print(f'\t{self.generated_files} generated files')

    def check_files(self, files: list) -> list:
        """Check existing files with correct extension and return only valid files"""
        files = Common.check_existing_files(files)
        files = Common.check_files_extention(files, ['musicxml', 'mscx'])

        return list(set(files))

    def get_params_of_tags(self, tree: etree.Element, tag: str, param: str) -> list:
        """Get the ids of the tags."""
        params = []
        for child in tree.xpath(f'//{tag}'):
            params.append(child.get(param))
        return params

    def get_valid_ids(self, tree, file_type)-> list:
        """Get only valid ids of parts in the tree."""
        if file_type =='musicxml':
            score_part_ids = self.get_params_of_tags(tree,'score-part', 'id')
            part_ids = self.get_params_of_tags(tree, 'part', 'id')
            return Common.intersection(score_part_ids, part_ids)
        elif file_type =='mscx':
            parts_count = len(tree.xpath('//Part'))
            staff_count = len(tree.xpath('/museScore/Staff'))

            if parts_count == staff_count:
                return self.get_params_of_tags(tree, '/museScore/Staff', 'id')
            else:
                return []

    def remove_credits_and_stuff(self, tree: etree.Element) -> etree.Element:
        """Remove unwanted elements (credits, lyrics, labels and dynamics) from XML tree.

        NOTE: NOT tested on MSCX files!
        """
        for elem in tree.xpath('//credit'):
            parent = elem.getparent()
            parent.remove(elem)
        for elem in tree.xpath('//rights'):
            parent = elem.getparent()
            parent.remove(elem)
        for elem in tree.xpath('//lyric'):
            parent = elem.getparent()
            parent.remove(elem)
        for elem in tree.xpath('//part-name'):
            elem.text = ''
        for elem in tree.xpath('//instrument-name'):
            elem.text = ''
        for elem in tree.xpath('//part-abbreviation'):
            elem.text = ''
        for elem in tree.xpath('//direction'):
            parent = elem.getparent()
            parent.remove(elem)
        return tree


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-I", "--input-files", nargs='*', default=None,
        help="Input XML (musicxml + mscx) files to process.")
    parser.add_argument(
        "-i", "--input-folder", type=str, default=None,
        help="Input folder where to look for XML (musicxml + mscx) files to process.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='out',
        help="Output folder to write files to.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    splitter = PartSplitter(
        input_files=args.input_files,
        input_folder=args.input_folder,
        output_folder=args.output_folder)
    splitter()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
