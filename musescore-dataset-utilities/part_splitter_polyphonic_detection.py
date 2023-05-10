#!/usr/bin/python3.8
"""Load multi-part .musicxml files to, separate them to parts and detect polyphonic ones. 

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

            for i, part_id in enumerate(sorted(part_ids)):
                file_out = self.get_file_out_name(file_in, i)

                parts = file_tree.xpath(f'//part[@id="{part_id}"]')

                if parts:
                    if self.is_polyphonic_part(parts[0]):
                        self.polyphonic_parts.append((os.path.basename(file_out), self.chords, self.voices))
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

        if self.dual_staff_parts_count > 0:
            dual_staff_file = os.path.join(self.output_folder, '0_dual_staff_parts.json')
            print(f'\t{self.dual_staff_parts_count} dual staff parts '
                  f'(saved into {dual_staff_file})')

            if not os.path.exists(dual_staff_file):
                Common.write_to_file(self.dual_staff_parts, dual_staff_file)
            else:
                print(f'WARNING: {dual_staff_file} already exists, printing to stdout instead')    
                print(self.dual_staff_parts)

        if self.polyphonic_parts_count > 0:
            polyphonic_file = os.path.join(self.output_folder, '0_polyphonic_parts.json')
            print(f'\t{self.polyphonic_parts_count} polyphonic parts '
                  f'(saved into {polyphonic_file})')

            if not os.path.exists(polyphonic_file):
                Common.write_to_file(self.polyphonic_parts, polyphonic_file)
            else:
                print(f'WARNING: {polyphonic_file} already exists, printing to stdout instead')    
                print(self.polyphonic_parts)

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
        self.chords = len(chord_notes)

        voices = part.xpath('//measure/note/voice')
        voices = list(set([voice.text for voice in voices]))

        if len(voices) > 1:
            has_more_voices = True
        self.voices = len(voices)

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
        """Go though all measures with change new-page to new-system.
        
        Precise tags are: `<print new-page="yes" />` change to `<print new-system="yes" />`."""
        print_tags = tree.xpath('//measure/print[@new-page="yes"]')

        for print_tag in print_tags:
            print_tag.attrib.pop('new-page')
            print_tag.attrib['new-system'] = 'yes'

        return tree

    def separate_dual_staff(self, tree_orig: etree.Element, file_out: str) -> (etree.Element, str):
        """Seaparate dual staff part to two one staff parts. 
        
        Return second staff part and its file name to save.
        First staff part is updated here but doesn't have to be returned 
            for it to be saved back in __call__."""
        file_split = os.path.basename(file_out).split('.')[0]
        file_out = f'{file_split}a.musicxml'
        file_out = os.path.join(self.output_folder, file_out)

        new_tree = deepcopy(tree_orig)

        self.dual_staff_separate_first(tree_orig)

        self.dual_staff_separate_second(new_tree)

        return new_tree, file_out

    def dual_staff_separate_first(self, part: etree.Element) -> None:
        """Remove second staff."""
        staves = part.xpath('.//measure[@number=1]/attributes/staves')
        if staves:
            staves[0].text = "1"

        clefs = part.xpath('.//measure[@number=1]/attributes/clef[@number=2]')
        if clefs:
            clefs[0].getparent().remove(clefs[0])

        second_staff_notes = part.xpath('.//measure/note[staff="2"]')
        for note in second_staff_notes:
            note.getparent().remove(note)

    def dual_staff_separate_second(self, part: etree.Element) -> None:
        """Remove first staff."""
        staves = part.xpath('.//measure[@number=1]/attributes/staves')
        if staves:
            staves[0].text = "1"

        clefs = part.xpath('.//measure[@number=1]/attributes/clef')
        if len(clefs) > 1:
            clefs[0].getparent().remove(clefs[0])
            clefs[1].attrib['number'] = '1'

        second_staff_notes = part.xpath('.//measure/note[staff="1"]')
        for note in second_staff_notes:
            note.getparent().remove(note)

        second_staff_notes = part.xpath('.//measure/note/staff')
        for note in second_staff_notes:
            note.text = '1'


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
