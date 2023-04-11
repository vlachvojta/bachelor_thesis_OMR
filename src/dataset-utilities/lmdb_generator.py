#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# Starting code downloaded from:
# https://github.com/DCGM/pero-ocr/blob/master/user_scripts/parse_folder.py
# Authors on github: ibenes, michal-hradis, OldaKodym, xkissm00, kohuthonza

import argparse
import re
import os
import time
import lmdb

from common import Common


class LMDB_generator:

    exts1 = []
    exts2 = []
    in_folders = []
    output = ''

    gb100 = 100000000000

    def __init__(self, exts1: list = ['agnostic'],
                 exts2: list = ['png'], in_folders: list = ['.'],
                 output: str = '', ignore_texts: bool = False,
                 ignore_images: bool = False):
        self.exts1 = exts1
        self.exts2 = exts2
        self.in_folders = in_folders
        self.output = output
        self.ignore_texts = ignore_texts
        self.ignore_images = ignore_images

    def __call__(self) -> None:
        if not os.path.exists(self.output):
            os.mkdir(self.output)

        files1 = files2 = []

        if not self.ignore_texts:
            print('Exporting text to lmdb is deprecated because it list its use case.')
            # print('Getting all text file names')
            # files1 = Common.get_files_from_folders(
            #     self.in_folders, self.exts1[0], False)
        if not self.ignore_images:
            print('Getting all image file names')
            files2 = Common.get_files_from_folders(
                self.in_folders, self.exts2, False)

        if not self.ignore_images and not self.ignore_texts:
            n_file_groups_1 = len(files1) // len(self.exts1)
            n_file_groups_2 = len(files2) // len(self.exts2)
            assert n_file_groups_1 == n_file_groups_2

        # if not self.ignore_texts:
        #     self.files_to_lmdb_text(
        #         files1, os.path.join(self.output, 'texts.lmdb'))

        if not self.ignore_images:
            self.files_to_lmdb(files2, os.path.join(self.output, 'images.lmdb'))

    def files_to_lmdb(self, files: list = [], output: str = 'output.lmdb'):
        print(f'Writing {len(files)} files to {output} '
              '(every dot is 200 files, every line is 10_000 files)')

        lmdb_db = lmdb.open(output, map_size=self.gb100)

        for i, file in enumerate(files):
            Common.print_dots(i, 200, 10_000)
            file_name = re.split('/', file)[-1]
            file_id = re.split(r'\.', file_name)[0]
            file_ext = re.split(r'\.', file_name)[-1]

            key = f'{file_id}.{file_ext}'
            data = Common.read_file(file, lmdb=True)

            with lmdb_db.begin(write=True) as txn_out:
                c_out = txn_out.cursor()
                c_out.put(key.encode(), data)
        print('')

    def files_to_lmdb_text(self, files: list = [],
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
        "-E", "--extensions-images", nargs='*', default=['png'],
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
        help="Ignore texts, don't generate text lmdb for files with exts1.")
    parser.add_argument(
        "-i", "--ignore-images", default=False, action="store_true",
        help=("Ignore images, " +
              "don't generate byte-form lmdb for files with exts2"))

    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    generator = LMDB_generator(
        exts1=args.extensions_text,
        exts2=args.extensions_images,
        in_folders=args.src_folders,
        output=args.output_folder,
        ignore_texts=args.ignore_texts,
        ignore_images=args.ignore_images)

    generator()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
