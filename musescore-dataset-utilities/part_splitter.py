#!/usr/bin/python3.8
"""Split multi-part .musicxml files to multiple files with only one part per file.

Script also rem eloves unwantedements in remove_unwanted_elements function.

File naming conventions: file.musicxml -> file_p[1-n].musicxml
    where n is the number of parts.

Usage:
$ python3 part_splitter.py -i 100.musicxml -o parts_out/
resulting in creating files parts_out/100_p00.musicxml, parts_out/100_p01.musicxml etc.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
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
    def __init__(self, input_files: list = None, input_folder: str = None,
                 staves_on_page: int = 8, output_folder: str = 'out'):
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
        self.no_complete_pages_parts = []

        self.generated_files = 0

        self.staves_on_page = staves_on_page

    def __call__(self):
        print(f'Going through {len(self.input_files)} files. '
              '(every dot is 200 files, every line is 2_000)')

        for i, file_in in enumerate(self.input_files):
            Common.print_dots(i, 200, 2_000)

            try:
                file_tree = etree.parse(file_in)
            except etree.XMLSyntaxError:
                self.xml_syntax_error_files += 1
                continue

            part_ids = self.get_valid_ids(file_tree)
            if not part_ids:
                self.music_score_error_files += 1
                continue

            self.remove_unwanted_elements(file_tree)

            for i, part_id in enumerate(sorted(part_ids)):
                file_out = self.get_file_out_name(file_in, i)

                # Create new root tag and add children from file_tree
                root_tag = '<score-partwise version="4.0"></score-partwise>'
                new_tree = etree.fromstring(root_tag)
                for i, child in enumerate(list(file_tree.getroot())):
                    if child.tag == 'part':
                        continue
                    child_str = etree.tostring(child)
                    child_back = etree.fromstring(child_str)
                    new_tree.insert(i+1, child_back)

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
                        new_tree.insert(7, part_copy)

                result = self.change_new_page_to_new_system(new_tree)
                if not result:
                    self.no_complete_pages_parts.append(os.path.basename(file_out))
                    continue

                # Ignore percussion parts
                if self.is_percussion_part(new_tree):
                    continue

                # Detect multi staff and polyphonic parts
                if self.get_number_of_staves(new_tree) > 1:
                    self.dual_staff_parts.append(os.path.basename(file_out))
                    self.dual_staff_parts_count += 1
                    new_trees, files_out = self.separate_multiple_staff_part(new_tree, file_out)
                else:
                    new_trees = [new_tree]
                    files_out = [file_out]

                for new_tree, file_out in zip(new_trees, files_out):
                    self.save_part_to_file(new_tree, file_out)

                    if self.is_polyphonic_part(new_tree):
                        self.polyphonic_parts.append(os.path.basename(file_out))
                        self.polyphonic_parts_count += 1

        self.print_results()

    def save_part_to_file(self, tree: etree.Element, file_out: str):
        tree.getroottree().write(file_out, pretty_print=True, encoding='utf-8')
        self.generated_files += 1

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

        # TODO delete dual staff parts stats??
        if self.dual_staff_parts_count > 0:
            dual_staff_file = os.path.join(self.output_folder, '0_dual_staff_parts.json')
            print(f'\t{self.dual_staff_parts_count} dual staff parts '
                  f'(saved into {dual_staff_file})')

            # TODO test this
            if not os.path.exists(dual_staff_file):
                Common.write_to_file(self.dual_staff_parts, dual_staff_file)
            else:
                # TODO concat existing file to new and save
                print(f'WARNING: {dual_staff_file} already exists, printing to stdout instead')    
                print(self.dual_staff_parts)

        if self.polyphonic_parts_count > 0:
            polyphonic_file = os.path.join(self.output_folder, '0_polyphonic_parts.json')
            print(f'\t{self.polyphonic_parts_count} polyphonic parts '
                  f'(saved into {polyphonic_file})')

            # TODO test this
            if not os.path.exists(polyphonic_file):
                Common.write_to_file(self.polyphonic_parts, polyphonic_file)
            else:
                # TODO concat existing file to new and save
                print(f'WARNING: {polyphonic_file} already exists, printing to stdout instead')    
                print(self.polyphonic_parts)

        if self.no_complete_pages_parts > 0:
            out_file_name = os.path.join(self.output_folder, '0_no_complete_pages_parts.json')
            print(f'\t{len(self.no_complete_pages_parts)} no complete pages parts '
                  f'(saved into {out_file_name})')

            # TODO test this
            if not os.path.exists(out_file_name):
                Common.write_to_file(self.no_complete_pages_parts, out_file_name)
            else:
                # TODO concat existing file to new and save
                print(f'WARNING: {out_file_name} already exists, printing to stdout instead')    
                print(self.no_complete_pages_parts)

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

    def remove_unwanted_elements(self, tree: etree.Element) -> None:
        """Remove unwanted elements (credits, lyrics, labels and dynamics) from XML tree.
        """
        elements_to_remove = [
            'credit', 'rights', 'lyric', 'direction', 'creator', 'work', 'part-group', 'notations'
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

    def get_number_of_staves(self, part: etree.Element) -> bool:
        """Check if part is a dual staff part using "<attributes>" tag in the first measure."""
        staves = part.xpath('//measure[@number=1]/attributes/staves')

        if staves:
            number = staves[0].text
            try:
                number = int(number)
                if number > 1:
                    return number
            except ValueError:
                print(f'WARNING: Number of staves in first measure cannot be parsed to int. '
                      f'({number})')
                return 1

        return 1

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

    def change_new_system_to_new_page(self, tree: etree.Element) -> etree.Element:
        """Go though all measures with change new-page to new-system.
        
        Precise tags are: `<print new-page="yes" />` change to `<print new-system="yes" />`."""
        print_tags = tree.xpath('//measure/print[@new-system="yes"]')

        for print_tag in print_tags:
            print_tag.attrib.pop('new-system')
            print_tag.attrib['new-page'] = 'yes'

        return tree

    def change_new_page_to_new_system(self, tree: etree.Element) -> etree.Element:
        """Go though all measures, change new-page to new-system.
        
        Every n-th new-system change back to new-page.        
        Precise tags are: `<print new-page="yes" />` change to `<print new-system="yes" />`."""
        print_tags = tree.xpath('//measure/print[@new-page="yes"]')

        for print_tag in print_tags:
            print_tag.attrib.pop('new-page')
            print_tag.attrib['new-system'] = 'yes'

        print_tags = tree.xpath('//measure/print[@new-system="yes"]')

        if len(print_tags) == 0:
            return False

        # if Last page is NOT copmlete, delete it
        if not len(print_tags) - 1 % self.staves_on_page == self.staves_on_page - 1:
            extra_systems = len(print_tags) % self.staves_on_page + 1
            # print(f'extra_systems: {extra_systems}')
            # print(f'len(print_tags): {len(print_tags)}')

            if extra_systems >= len(print_tags):
                # part doesn't have even one complete page
                measures_to_delete = tree.xpath(f'//measure')
                return False
            else:
                first_measure_to_delete = print_tags[-extra_systems].getparent().get('number')
                measures_to_delete = tree.xpath(f'//measure[@number>={first_measure_to_delete}]')

            for measure in measures_to_delete:
                measure.getparent().remove(measure)

        for i, print_tag in enumerate(print_tags):
            # Every n-th new-system change to new-page. N is staves_on_page
            # (the first system in the score doesn't have a new-system tag)
            if i % self.staves_on_page == self.staves_on_page - 1:
                print_tag.attrib.pop('new-system')
                print_tag.attrib['new-page'] = 'yes'

        return True

    def separate_multiple_staff_part(self, tree_orig: etree.Element, file_out_orig: str
                                    ) -> (list, list):
        """Seaparate multiple staff part to one staff parts.

        Return tuple:
            first value: all separated part trees
            second value: output file names
        """
        staves = self.get_number_of_staves(tree_orig)
        # print(f'staves: {staves}')

        file_split = os.path.basename(file_out_orig).split('.')[0]
        file_out_names = []

        for i in range(staves):
            file_out = f"{file_split}{chr(ord('a') + i)}.musicxml"
            file_out_names.append(os.path.join(self.output_folder, file_out))

        part_trees = [tree_orig]
        for _ in range(staves - 1):
            part_trees.append(deepcopy(tree_orig))

        for i, part_tree in enumerate(part_trees, start=1):
            # print(f'separating staff number: {i}')
            self.separate_specific_part(part_tree, i)

        return part_trees, file_out_names

    def separate_specific_part(self, part: etree.Element, staff_to_leave: int) -> None:
        """Separate one staff from whole part. Remove the others."""
        staves = part.xpath('.//measure[@number=1]/attributes/staves')
        if staves:
            staves[0].text = "1"

        staff_layouts = part.xpath('.//measure/print/staff-layout')
        for layout in staff_layouts:
            layout.getparent().remove(layout)

        clefs = part.xpath('.//measure[@number=1]/attributes/clef')
        if len(clefs) > 1:
            for i, clef in enumerate(clefs, start=1):
                if i == staff_to_leave:
                    clef.attrib['number'] = '1'
                else:
                    clef.getparent().remove(clef)

        notes = part.xpath('.//measure/note')
        for note in notes:
            staff = note.xpath('.//staff')[0]
            if int(staff.text) == staff_to_leave:
                staff.text = '1'
            else:
                note.getparent().remove(note)


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
        "-s", "--staves-on-page", type=int, default=8,
        help="How many staves should be on one page.")
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
        staves_on_page=args.staves_on_page,
        output_folder=args.output_folder)
    splitter()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
