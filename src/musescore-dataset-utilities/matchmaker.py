#!/usr/bin/python3.8
"""Get label-image pairs from two separate folders

Usage:
$ python3 matchmaker.py --labels 5_labels --images 4_images -o 6_pairs
Resulting in copying pairs of labels and images to folder 6_pairs.
"""

import argparse
import re
import sys
import os
import time
import logging

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class Matchmaker:
    """Get label-image pairs from two separate folders"""
    def __init__(self, labels_folder: list = '.', images_folder: str = '.',
                 output_folder: str = 'pairs', verbose: bool = False):
        self.labels_folder = labels_folder
        self.images_folder = images_folder
        self.output_folder = output_folder
        self.verbose = verbose

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO,format='[%(levelname)-s]\t- %(message)s')
        
        self.images = Common.listdir(self.images_folder, ['png'])
        self.labels = Common.listdir(self.labels_folder, ['semantic'])

        if not self.images:
            print('No valid IMAGES in given folder.')
        if not self.labels:
            print('No valid LABELS in given folder.')

        print(f'Found {len(self.images)} image file.')
        print(f'Found {len(self.labels)} label files.')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # self.suspicious_files = []
        # self.generated_staves = 0

    def __call__(self):
        image_parts = [self.get_part_name(img) for img in self.images]
        label_parts = [self.get_part_name(label) for label in self.labels]

        image_parts = self.list_to_dict_sum(image_parts)
        label_parts = self.list_to_dict_sum(label_parts)

        print(len(image_parts))
        print(len(label_parts))
        print(image_parts)
        print(label_parts)

        pairs = {}

        for part_name, n in image_parts.items():
            if part_name in label_parts:
                pairs[part_name] = [label_parts[part_name], image_parts[part_name]]
                print(f'{part_name}: \t(i: {image_parts[part_name]}, l: {label_parts[part_name]})')



        # for i, file in enumerate(self.input_files):
        #     if i % 1000 == 0:
        #         suspicious_files_path = os.path.join(self.output_folder, '0_suspicious_files.json')
        #         print(f'\t{len(self.suspicious_files)} files was suspicious, writing to file.')
        #         Common.write_to_file(self.suspicious_files, suspicious_files_path)
        #     if not self.verbose:
        #         Common.print_dots(i, 200, 8_000)
        #     logging.debug('Working with: %d, %s', i, file)


        # self.print_results()

    def get_part_name(self, file: str):
        """Get file name, return part name."""
        file = os.path.basename(file)
        mscz_id, part_id, *_ = re.split(r'_|-', file)
        # print(f'mscz: {mscz_id}, part: {part_id}, rest: {rest}')

        return f'{mscz_id}_{part_id}'

    def list_to_dict_sum(self, parts: list) -> dict:
        """Get list with duplicate values, return sum of occurences in dict."""
        sums = {}
        processed_parts = set()

        for part in parts:
            if part in processed_parts:
                sums[part] += 1
            else:
                processed_parts.add(part)
                sums[part] = 1
        return sums


    # def print_results(self):
    #     """Print stats for input and output files."""
    #     print('')
    #     print('--------------------------------------')
    #     print('Results:')
    #     print(f'From {len(self.input_files)} input files:')
    #     print(f'\t{self.generated_staves} generated staves.')

    #     if len(self.suspicious_files) > 0:
    #         self.suspicious_files = sorted(list(set(self.suspicious_files)))
    #         print(f'\t{len(self.suspicious_files)} files was suspicious.')
    #         suspicious_files_path = os.path.join(self.output_folder, '0_suspicous_files.json')

    #         if not os.path.exists(suspicious_files_path):
    #             Common.write_to_file(self.suspicious_files, suspicious_files_path)
    #         else:
    #             # TODO concat existing file to new and save
    #             print(f'WARNING: {suspicious_files_path} already exists, '
    #                   'printing to stdout instead')
    #             print(self.suspicious_files)


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--images-folder", type=str, default='.',
        help="Input folder where to look for images.")
    parser.add_argument(
        "-l", "--labels-folder", type=str, default='.',
        help="Input folder where to look for labels.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='out',
        help="Output folder to copy complete pairs.")
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    cutter = Matchmaker(
        images_folder=args.images_folder,
        labels_folder=args.labels_folder,
        output_folder=args.output_folder,
        verbose=args.verbose)
    cutter()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
