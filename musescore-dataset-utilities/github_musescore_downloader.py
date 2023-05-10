#!/usr/bin/python3.8
"""Download musescore files from github repo given the link of repo and the list of files.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import argparse
import re
import sys
import os
import time
import shutil
import requests

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class GithubDownloader:
    """Download musescore files from github repo."""
    def __init__(self, link: str, file_list=str, output_folder: str = '0_orig_mscz'):
        self.link = link
        self.output_folder = output_folder

        # Load file names from input file
        if not os.path.exists(file_list):
            print('ERROR: Could not find musescore file list.')
            return
        self.files_to_download = re.split(r'\n', Common.read_file(file_list))
        self.files_to_download = list(filter(None, self.files_to_download))
        self.files_to_download = [f for f in self.files_to_download 
                                  if not os.path.exists(self.get_output_file_name(f))]

        # Create output part if necessary
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def __call__(self):
        print(f'Downloading {len(self.files_to_download)} files. ')

        for i, file_name in enumerate(self.files_to_download):
            for folder in range(20):
                url = f'{self.link}/{folder}/{file_name}.mscz'

                try:
                    response = requests.get(url, stream=True, timeout=20)
                except TimeoutError:
                    print(f'Download time out: {file_name}')
                    continue
                except ConnectionError:
                    print(f'Connection error: {file_name}')
                    continue

                if response.headers['content-type'] == 'text/html; charset=utf-8':
                    continue

                output_file = self.get_output_file_name(file_name)
                with open(output_file, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                print(f'{folder}/{file_name}')
                break

    def get_output_file_name(self, file):
        """Get output file name from file and output folder."""
        return os.path.join(self.output_folder, f'{file}.mscz')


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--link", required=True,
        help="Link to github repo were folders with musescore files are stored.")
    parser.add_argument(
        "-f", "--file-list", required=True,
        help="File with a list of mscz file to download.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='0_orig_mscz',
        help="Output folder to save downloaded files to.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    downloader = GithubDownloader(
        link=args.link,
        file_list=args.file_list,
        output_folder=args.output_folder)
    downloader()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()

