#!/usr/bin/python3.8
"""Split multi-part .musicxml files to multiple files with only one part per file.

Script also removes unwanted elements in remove_credits_and_stuff function.

File naming conventions: file.musicxml -> file_p[1-n].musicxml
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

        self.dual_staff_parts_count = 0
        self.dual_staff_parts = []
        self.polyphonic_parts_count = 0
        self.polyphonic_parts = []

        self.generated_files = 0

    def __call__(self):
        print(f'Going through {len(self.input_files)} files. (every dot is 200 files)')

        for i, file_in in enumerate(self.input_files):
            Common.print_dots(i, 200, 8_000)

            try:
                file_tree = etree.parse(file_in)
            except etree.XMLSyntaxError:
                self.xml_syntax_error_files += 1
                continue

            part_ids = self.get_valid_ids(file_tree)
            if not part_ids:
                self.music_score_error_files += 1
                continue

            self.remove_credits_and_stuff(file_tree)

            # Create new root tag and add children from file_tree
            root_tag = '<score-partwise version="4.0"></score-partwise>'
            file_headers = etree.fromstring(root_tag)
            for i, child in enumerate(list(file_tree.getroot())):
                if child.tag == 'part':
                    continue
                child_str = etree.tostring(child)
                child_back = etree.fromstring(child_str)
                file_headers.insert(i+1, child_back)

            files_headers_str = etree.tostring(file_headers)

            new_trees = [file_headers]
            for _ in range(len(part_ids) - 1):
                new_trees.append(etree.fromstring(files_headers_str))
                # new_trees.append(deepcopy(file_tree))

            for i, (part_id, new_tree) in enumerate(zip(sorted(part_ids), new_trees)):
                file_out = self.get_file_out_name(file_in, i)

                # Remove all other part declarations
                score_parts = new_tree.xpath('//score-part')
                for part in score_parts:
                    if part.get('id') != part_id:
                        part.getparent().remove(part)

                # Insert only the right part directly from original file_tree
                parts = file_tree.xpath('//part')
                for part in parts:
                    if part.get('id') == part_id:
                        part_copy = deepcopy(part)
                        # part_str = etree.tostring(part)
                        # part_copy = etree.fromstring(part_str)
                        new_tree.insert(7, part_copy)

                new_tree = self.change_new_page_to_new_system(new_tree)

                current_part = new_tree.xpath(f'//part[@id="{part_id}"]')[0]

                # Ignore percussion parts
                if self.is_percussion_part(current_part):
                    continue

                # Report dual staff part if needed
                if self.is_dual_staff_part(current_part):
                    self.dual_staff_parts.append(os.path.basename(file_out))
                    self.dual_staff_parts_count += 1

                if self.is_polyphonic_part(current_part):
                    self.polyphonic_parts.append(os.path.basename(file_out))
                    self.polyphonic_parts_count += 1

                # Save every part to a special file
                new_tree.getroottree().write(file_out, pretty_print=True, encoding='utf-8')
                self.generated_files += 1

        self.print_results()

    def get_file_out_name(self, name, part_id):
        """Get file in name, part id a return name for output file WITH PATH."""
        file_split = os.path.basename(name).split('.')[0]
        file_out = f'{file_split}_p{part_id:02d}.musicxml'
        return os.path.join(self.output_folder, file_out)

    def print_results(self):
        print('')
        print('--------------------------------------')
        print('Results:')
        print(f'From {len(self.input_files)} input files:')
        print(f'\t{self.generated_files} generated part files')
        print(f'\t{self.xml_syntax_error_files} had xml syntax errors')
        print(f'\t{self.music_score_error_files} had music score errors')

        if self.dual_staff_parts_count > 0:
            dual_staff_file = os.path.join(self.output_folder, '0_dual_staff_parts.json')
            print(f'\t{self.dual_staff_parts_count} dual staff parts '
                  f'(saved into {dual_staff_file})')
            Common.write_to_file(self.dual_staff_parts, dual_staff_file)

        if self.polyphonic_parts_count > 0:
            polyphonic_file = os.path.join(self.output_folder, '0_polyphonic_parts.json')
            print(f'\t{self.polyphonic_parts_count} polyphonic parts '
                  f'(saved into {polyphonic_file})')
            Common.write_to_file(self.polyphonic_parts, polyphonic_file)

    def check_files(self, files: list) -> list:
        """Check existing files with correct extension and return only valid files"""
        files = Common.check_existing_files(files)
        files = Common.check_files_extention(files, ['musicxml'])

        files_uniq = list(set(files))
        if len(files_uniq) < len(files):
            print(f'WARNING: {len(files) - len(files_uniq)} duplicate files.')

        return files

    def get_params_of_tags(self, tree: etree.Element, tag: str, param: str) -> list:
        """Get the ids of the tags."""
        params = []
        for child in tree.xpath(f'//{tag}'):
            params.append(child.get(param))
        return params

    def get_valid_ids(self, tree)-> list:
        """Get only valid ids of parts in the tree."""
        score_part_ids = self.get_params_of_tags(tree,'score-part', 'id')
        part_ids = self.get_params_of_tags(tree, 'part', 'id')
        return Common.intersection(score_part_ids, part_ids)

    def remove_credits_and_stuff(self, tree: etree.Element) -> None:
        """Remove unwanted elements (credits, lyrics, labels and dynamics) from XML tree.
        """
        elements_to_remove = [
            'credit', 'rights', 'lyric', 'direction', 'creator', 'work', 'part-group'
        ]

        for elem in elements_to_remove:
            self.remove_element(tree, elem)

        for elem in tree.xpath('//part-name'):
            elem.text = ''
        for elem in tree.xpath('//instrument-name'):
            elem.text = ''
        for elem in tree.xpath('//part-abbreviation'):
            elem.text = ''
    
    def remove_element(self, tree: etree.Element, element: str) -> None:
        """Remove all element by name from given tree."""
        for elem in tree.xpath(f'//{element}'):
            elem.getparent().remove(elem)

    def is_dual_staff_part(self, part: etree.Element) -> bool:
        """Check if part is a dual staff part using "<attributes>" tag in the first measure."""
        staves = part.xpath('//measure[@number=1]/attributes/staves')

        if staves:
            number = staves[0].text
            try:
                number = int(number)
                if number > 1:
                    return True
            except ValueError:
                print(f'WARNING: Number of staves in first measure cannot be parsed to int. '
                      f'({number})')
                return True

        return False

    def is_percussion_part(self, part: etree.Element) -> bool:
        """Check if part is percussion part using "<clef><sign>percussion" tag."""
        # clef_signs = part.xpath('//measure[@number=1]/clef/sign')
        clef_signs = part.xpath('//measure[@number=1]/attributes/clef/sign')

        if clef_signs and clef_signs[0].text == 'percussion':
            return True

        return False

    def is_polyphonic_part(self, part: etree.Element) -> bool:
        """Look for <chord/> tag in notes to determine whether part is polyphonic."""
        has_chords = False
        has_more_voices = False

        chord_notes = part.xpath('//measure/note/chord')

        if len(chord_notes) > 0:
            has_chords = True

        voices = part.xpath('//measure/note/voice')
        voices = list(set([voice.text for voice in voices]))

        if len(voices) > 1:
            has_more_voices = True

        return has_chords or has_more_voices

    def change_new_page_to_new_system(self, tree: etree.Element) -> etree.Element:
        """Go though all measures with change new-page to new-system.
        
        Precise tags are: `<print new-page="yes" />` change to `<print new-system="yes" />`."""
        print_tags = tree.xpath('//measure/print[@new-page="yes"]')

        for print_tag in print_tags:
            print_tag.attrib.pop('new-page')
            print_tag.attrib['new-system'] = 'yes'

        return tree


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-I", "--input-files", nargs='*', default=None,
        help="Input musicxml files to process.")
    parser.add_argument(
        "-i", "--input-folder", type=str, default=None,
        help="Input folder where to look for musicxml files to process.")
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
