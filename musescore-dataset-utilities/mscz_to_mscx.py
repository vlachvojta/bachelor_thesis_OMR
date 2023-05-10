#!/usr/bin/python3.8
"""Simple script to extract mscx file from mscz (zip) file

Example run:
$ python3 mscz_to_mscx.py --input-files folder/*.mscz --output-folder out
"""

import argparse
import re
import sys
import os
import time
import zipfile
# import numpy as np
# import matplotlib.pyplot as plt
# from customwer import CustomWer

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


MUSESCORE_FILE_TYPE = 'mscz'
MUSICXML_FILE_TYPE = 'mscx'


class MsczToMscx:
    def __init__(self, input_files, output_folder) -> None:
        self.input_files = input_files
        self.output_folder = output_folder

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        existing_files = []

        for file in input_files:
            if (os.path.exists(file) and os.path.isfile(file)
                and file.endswith(MUSESCORE_FILE_TYPE)):
                existing_files.append(file)
        
        print(f'Found {len(existing_files)} existing files: {existing_files}')

        for file_in in existing_files:
            with zipfile.ZipFile(file_in, 'r') as zip_file:
                file_out = [file for file in zip_file.namelist() 
                            if file.endswith(MUSICXML_FILE_TYPE)]
                # print(file_out)

                # info = archive.infolist()
                if len(file_out) == 1:
                    file_out = file_out[0]
                elif len(file_out) > 1:
                    raise FileExistsError(
                        f'ERROR: More than one file found in {file_in}')
                elif len(file_out) == 0:
                    print(f'WARNING: No file found in {file_in}')
                    continue

                #zip_file.extract(f'{file_in_name}.{MUSICXML_FILE_TYPE}', os.path.dirname(file_in))
                file_out = zip_file.read(file_out).decode('utf-8')
                # print(file_out[:100])

            file_in_name = os.path.basename(file_in).split(".")[0]

            file_out_name = os.path.join(output_folder, f'{file_in_name}.{MUSICXML_FILE_TYPE}')

            with open(file_out_name, 'w', encoding='utf-8') as f:
                f.write(file_out)

            print(f'File saved to {file_out_name}')
            # print(f'type(mscx): {type(mscx)}, len(mscx): {len(mscx)}')


def parseargs():
    """Parse arguments."""
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-files", nargs='+',
        help="Input files")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='out',
        help="Output folder to write outputs to.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    MsczToMscx(
        input_files=args.input_files,
        output_folder=args.output_folder)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
