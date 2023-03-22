#!/usr/bin/python3.8
"""List suspicious files with given parameters from list file.

Usage:
$ python3 suspicious_files_lister.py -i suspicious_files_list.txt -m whole
Resulting in printing subset of files sorted by size for given mode.
"""

import argparse
import re
import sys
import os
import time
# import logging

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class SusLister:
    """List suspicious files with given parameters from list file."""
    def __init__(self, sus_list_file: str, mode: str = 'whole'):
        self.sus_list_file = sus_list_file
        self.mode = mode

        self.sus_list = Common.read_file(self.sus_list_file)
        self.sus_list = re.split(r'\n', self.sus_list)
        # filter out empty lines
        self.sus_list = list(filter(None, self.sus_list))

        self.sus_list = Common.check_files(self.sus_list, ['png'])

    def __call__(self):
        files_with_sizes = []

        for file in self.sus_list:
            size = os.path.getsize(file) // 1000    # size in kb
            part = self.get_part_name_with_suspicious(file)

            dirs = re.split(r'/|\\', file)[:-1]
            path_to_file = '/'.join(dirs)

            files_with_sizes.append((part, path_to_file, size))
            # print(f'{(part, path_to_file, size)}')

        # sort according to part name
        files_with_sizes.sort(key=lambda x: x[0])

        # Aggregate parts
        parts_with_sizes = {}
        processed_parts = set()

        for part, dir, size in files_with_sizes:
            if part in processed_parts:
                _, orig_size = parts_with_sizes[part]
                parts_with_sizes[part] = (dir, orig_size + size)
            else:
                processed_parts.add(part)
                parts_with_sizes[part] = (dir, size)

        parts_with_sizes_list = []
        for part, (dir, size) in parts_with_sizes.items():
            parts_with_sizes_list.append((part, dir, size))

        parts_with_sizes = parts_with_sizes_list


        # sort according to size
        parts_with_sizes.sort(key=lambda x: x[2], reverse=True)

        # for part_with_info in parts_with_sizes:
        #     print(part_with_info)

        part_names = [part for part, _, _ in parts_with_sizes]
        uniq_part_names = list(set(part_names))
        assert len(part_names) == len(uniq_part_names), "Duplicate part names found."
        # print(f'len(uniq_part_names): {len(uniq_part_names)}')

        # Print output list
        if self.mode == 'whole':
            for part, dir, _ in parts_with_sizes:
                print(f'{dir}/{part}.musicxml')
        elif self.mode == 'short':
            # Aggregate mscz files
            mscz_with_sizes_list = [(p.split('_')[0], d, s) for p, d, s in parts_with_sizes]
            # print(mscz_with_sizes_list)

            mscz_with_sizes = {}
            processed_msczs = set()

            for part, dir, size in mscz_with_sizes_list:
                if part in processed_msczs:
                    _, orig_size = mscz_with_sizes[part]
                    mscz_with_sizes[part] = (dir, orig_size + size)
                else:
                    processed_msczs.add(part)
                    mscz_with_sizes[part] = (dir, size)

            mscz_with_sizes_list = []
            for part, (dir, size) in mscz_with_sizes.items():
                mscz_with_sizes_list.append((part, dir, size))

            mscz_with_sizes = mscz_with_sizes_list

            print(len(mscz_with_sizes))
            for mscz_file, *_ in mscz_with_sizes:
                print(mscz_file)

            # sort according to size
            mscz_with_sizes.sort(key=lambda x: x[2], reverse=True)
            
            # print(number)
        elif self.mode == 'orig_musicxml':
            number = re.split(r'_', part)[0]
            print(f'{dir}/{number}.musicxml')

        # self.images = [os.path.basename(image) for image in self.images]
        # self.labels = [os.path.basename(label) for label in self.labels]

        # print(len(self.images))
        # lent = len(self.images)
        # print(sorted(self.images)[lent-20:])

        # image_parts = [self.get_part_name(img) for img in self.images]
        # label_parts = [self.get_part_name(label) for label in self.labels]

        # print('---------------------')
        # print(len(image_parts))
        # print(sorted(image_parts))

        # image_parts = self.list_to_dict_sum(image_parts)
        # label_parts = self.list_to_dict_sum(label_parts)

        # print(len(image_parts))
        # # print(len(label_parts))
        # print(image_parts)
        # # print(label_parts)

        # pairs = {}

        # for part_name, n in image_parts.items():
        #     if part_name in label_parts:
        #         pairs[part_name] = [label_parts[part_name], image_parts[part_name]]
        #         print(f'{part_name}: \t(i: {image_parts[part_name]}, l: {label_parts[part_name]})')



        # for i, file in enumerate(self.input_files):
        #     if i % 1000 == 0:
        #         suspicious_files_path = os.path.join(self.output_folder, '0_suspicious_files.json')
        #         print(f'\t{len(self.suspicious_files)} files was suspicious, writing to file.')
        #         Common.write_to_file(self.suspicious_files, suspicious_files_path)
        #     if not self.verbose:
        #         Common.print_dots(i, 200, 8_000)
        #     logging.debug('Working with: %d, %s', i, file)


        # self.print_results()

    # def get_part_name(self, file: str):
    #     """Get file name, return part name."""
    #     mscz_id, part_id, *_ = re.split(r'_|-', file)
    #     # print(f'mscz: {mscz_id}, part: {part_id}, rest: {rest}')

    #     return f'{mscz_id}_{part_id}'

    def get_part_name_with_suspicious(self, file: str):
        """Get file name, return part name."""
        file = os.path.basename(file)

        if file[0] == 'z':
            z, mscz_id, part_id, *_ = re.split(r'_|-', file)
        else:
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
        "-s", "--sus-list-file", type=str, default='.',
        help="List of sus files.")
    parser.add_argument(
        "-m", "--mode", type=str, default='whole', choices=['whole', 'short', 'part', 'orig_musicxml'],
        help="Input mode of output of the files. (just simple str operations)")
    # parser.add_argument(
    #     "-n", "--n-files", type=str, default='.',
    #     help="Count of files to output.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    lister = SusLister(
        sus_list_file=args.sus_list_file,
        mode=args.mode)
    lister()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
