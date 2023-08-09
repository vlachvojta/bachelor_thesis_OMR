#!/usr/bin/env python3.8
"""Script for retrieving stuff from existing LMDB Database. Needs keys to retrieve stuff.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import argparse
import re
import os
import sys
import time

import numpy as np
import logging
import lmdb
import cv2 as cv

from common import Common


def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l", "--lmdb-file", required=True, type=str,
        help="LMDB file to read")
    parser.add_argument(
        "-k", "--keys", nargs='*', type=str,
        help="Key to retrieve. Add more keys by add more -k arguments.")
    parser.add_argument(
        "-f", "--keys-files", nargs='*',
        help="Keys to retrieve in txt files. Add more keys by add more -f arguments.")
    parser.add_argument(
        "-o", "--output-folder", default='output_folder',
        help="Set output file with extension. Output format is JSON")
    parser.add_argument(
        "-v", "--verbose", action='store_true', default=False,
        help="Verbose mode")

    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    LmdbReader(
        lmdb_file=args.lmdb_file,
        keys=args.keys,
        keys_files=args.keys_files,
        output_folder=args.output_folder,
        verbose=args.verbose)()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


class LmdbReader:
    """Class for retrieving stuff from existing LMDB Database. Needs keys to retrieve stuff."""
    def __init__(self, lmdb_file: str, keys=None, keys_files=None, output_folder: str = 'output_folder',
                 verbose: bool = False):
        if not os.path.exists(lmdb_file):
            raise FileNotFoundError(f'LMDB file ({lmdb_file}) not found')
        self.lmdb_file = lmdb_file
        self.keys = LmdbReader.get_all_keys(keys, keys_files)

        self.output_folder = output_folder
        Common.prepare_output_folder(self.output_folder)

        self.verbose = verbose

        # Doesn't work for some reason...
        # if verbose:
        #     logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]  \t- %(message)s')
        # else:
        #     logging.basicConfig(level=logging.INFO, format='[%(levelname)-s]\t- %(message)s')

    def __call__(self):
        for key in self.keys:
            image_data = self.read_lmdb_key(key)
            self.write_image(image_data, key)

    def read_lmdb_key(self, key: str):
        lmdb_env = lmdb.open(self.lmdb_file)

        with lmdb_env.begin() as txn:
            with txn.cursor() as curs:
                print(f'Reading key ({key}) from file ({self.lmdb_file})')

                # For decoding byte sings use:
                # print(curs.get(key.encode()).decode())
                # For decoding text sings use:
                return curs.get(key.encode())

    def write_image(self, image_data, key):
        output_file = os.path.join(self.output_folder, key)
        # cv.imdecode(image_data, [int(cv.IMWRITE_JPEG_QUALITY), 95])

        decoded_image = cv.imdecode(np.frombuffer(image_data, np.uint8), cv.IMREAD_COLOR)
        # img = cv.imdecode(np.frombuffer(data, dtype=np.uint8), 1)  # From PERO

        Common.write_to_file(decoded_image, output_file)

    @staticmethod
    def get_all_keys(keys: list = None, keys_files: list = None) -> list:
        """Read all keys from keys_files and return appended with keys list."""
        if keys is None:
            keys = []
        if keys_files is None:
            keys_files = []

        for key_file in keys_files:
            keys += (Common.get_lines(key_file))

        if not keys:
            print('NO KEYS FOUND', file=sys.stderr)
        else:
            print(f'Found {keys} keys')

        return keys



if __name__ == '__main__':
    main()
