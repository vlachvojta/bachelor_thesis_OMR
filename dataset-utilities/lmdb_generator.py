#!/usr/bin/env python3.8
"""Script to take folder of images and encode it to LMDB database format to be used with PERO system.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import argparse
import re
import os
import time
import lmdb

from common import Common


class LMDB_generator:

    text_extensions = []
    image_extensions = []
    in_folders = []
    output = ''

    gb100 = 100000000000

    def __init__(self, text_extensions=None,
                 image_extensions=None, in_folders=None,
                 output: str = '', ignore_texts: bool = False,
                 ignore_images: bool = False,
                 create_list_file: bool = False):
        if in_folders is None:
            in_folders = ['.']
        if image_extensions is None:
            image_extensions = ['png']
        if text_extensions is None:
            text_extensions = ['agnostic']

        self.text_extensions = text_extensions
        self.image_extensions = image_extensions
        self.in_folders = in_folders
        self.output = output
        self.ignore_texts = ignore_texts
        self.ignore_images = ignore_images
        self.create_list_file = create_list_file

    def __call__(self) -> None:
        if not os.path.exists(self.output):
            os.mkdir(self.output)

        files1 = images = []

        if not self.ignore_texts:
            print('Exporting text to lmdb is deprecated because it lost its use case.')
            # print('Getting all text file names')
            # files1 = Common.get_files_from_folders(
            #     self.in_folders, self.text_extensions[0], False)
        if not self.ignore_images:
            print('Getting all image file names')
            images = Common.get_files_from_folders(
                self.in_folders, self.image_extensions, False)

        if not self.ignore_images and not self.ignore_texts:
            n_file_groups_1 = len(files1) // len(self.text_extensions)
            n_file_groups_2 = len(images) // len(self.image_extensions)
            assert n_file_groups_1 == n_file_groups_2

        # if not self.ignore_texts:
        #     self.files_to_lmdb_text(
        #         files1, os.path.join(self.output, 'texts.lmdb'))

        if not self.ignore_images:
            keys = self.images_to_lmdb(images, os.path.join(self.output, 'images.lmdb'))

            if self.create_list_file:
                list_file_name = os.path.join(self.output, 'list.semantic')
                list_file = ''
                for image in keys:
                    list_file += f'{image} 000000 "asdf"\n'
                Common.write_to_file(list_file, list_file_name)

    def images_to_lmdb(self, files: list, output: str = 'images.lmdb') -> list:
        """Embed all images to lmdb file. Return list of all IDs.
        """
        print(f'Writing {len(files)} files to {output} '
              '(every dot is 200 files, every line is 10_000 files)')

        lmdb_db = lmdb.open(output, map_size=self.gb100)
        keys = []

        for i, file in enumerate(files):
            Common.print_dots(i, 200, 10_000)
            file_name = re.split('/', file)[-1]
            file_id = re.split(r'\.', file_name)[0]
            file_ext = re.split(r'\.', file_name)[-1]

            key = f'{file_id}.{file_ext}'
            keys.append(key)
            data = Common.read_file(file, lmdb=True)

            with lmdb_db.begin(write=True) as txn_out:
                c_out = txn_out.cursor()
                c_out.put(key.encode(), data)
        print('')
        return keys

    def files_to_lmdb_text(self, files: list,
                           output: str = 'output_lmdb'):
        """OLD and deprecated. DO NOT USE."""
        print(f'Reading {len(files)} files (every dot is 1000 files)')

        data_to_export = {}

        for i, file in enumerate(files):
            Common.print_dots(i)
            file_name = re.split('/', file)[-1]
            file_id = re.split(r'\.', file_name)[0]

            key = f'{file_id}.png'
            data_to_export[key] = Common.read_file(file)
        print('')

        print(f'Writing {len(data_to_export.keys())} files')

        with open(output, 'w') as f:
            for k, v in data_to_export.items():
                f.write(f'{k} 000000 "{v}"\n')
        print('Writing to lmdb_text done')


def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-e", "--extensions-text", nargs='*', default=['agnostic'],
        help="Set file extensions for text files to be saved as text lmdb. ")
    parser.add_argument(
        "-E", "--extensions-images", nargs='*', default=['png', 'jpg'],
        help=("Set file extensions for image files "
              "to be saved as byte-form lmdb."))
    parser.add_argument(
        "-F", "--src-folders", nargs='*', default=['.'],
        help=("Directories where to look for files with given extensions. "
              "Use in combination with"
              " --extensions-text + --extensions-images."))
    parser.add_argument(
        "-o", "--output-folder", default='output_folder',
        help="Set output file with extension. Output format is JSON")
    parser.add_argument(
        "-t", "--ignore-texts", default=False, action="store_true",
        help="Ignore texts, don't generate text lmdb for files with text_extensions.")
    parser.add_argument(
        "-i", "--ignore-images", default=False, action="store_true",
        help=("Ignore images, " +
              "don't generate byte-form lmdb for files with image_extensions"))
    parser.add_argument(
        '-c', '--create-list-file', default=False, action='store_true',
        help='Create list file with image IDs and empty transcriptions, ready to be used with pero-ocr engine')

    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    LMDB_generator(
        text_extensions=args.extensions_text,
        image_extensions=args.extensions_images,
        in_folders=args.src_folders,
        output=args.output_folder,
        ignore_texts=args.ignore_texts,
        ignore_images=args.ignore_images,
        create_list_file=args.create_list_file)()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
