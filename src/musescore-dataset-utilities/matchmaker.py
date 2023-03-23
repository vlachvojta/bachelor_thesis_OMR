#!/usr/bin/python3.8
"""Get label-image pairs from two folders and copy to a new folder with corresponding names.

Part is complete when the number of images is equal to the number of labels and
part has not generated any suspicious images.

Image is suspicious a when whole page image was split
into images higher then threshold = it's not an image of one music stave but more.
In the input folder this is said by the image name starting with 'z'.

Usage:
$ python3 matchmaker.py --labels 5_labels/generated_labels.semantic --images 4_images -o 6_pairs
Resulting in copying pairs of labels and images to 6_pairs with new names.
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
    """Get label-image pairs from two separate folders."""
    def __init__(self, label_files: list, image_folder: list = ['.'],
                 output_folder: str = 'pairs', verbose: bool = False):
        self.label_files = label_files
        self.image_folder = image_folder
        self.output_folder = output_folder
        self.verbose = verbose

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO,format='[%(levelname)-s]\t- %(message)s')

        print(f'Loading labels from {len(self.label_files)} files.')
        # Load labels
        self.labels = []
        for label_file in label_files:
            self.labels += self.load_labels(label_file)
        if not self.labels:
            print('WARNING: No valid LABELS in given folder.')
        else:
            print(f'\tFound {len(self.labels)} labels.')

        # Load images from folders
        self.images = []
        sub_folders = [os.path.join(self.image_folder, folder)
                       for folder in os.listdir(self.image_folder)]
        image_folders = [folder for folder in sub_folders if os.path.isdir(folder)]
        image_folders += [self.image_folder]
        print(f'Looking for images in {len(image_folders)} folders')

        for image_folder in image_folders:
            self.images += Common.listdir(image_folder, ['png'])
        if not self.images:
            print('WARNING: No valid IMAGES in given folder.')
        else:
            print(f'\tFound {len(self.images)} image files.')

        # Create output part if necessary
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.not_fitting_staff_count = 0
        self.total_parts_found = set()
        self.extra_label_parts = set()
        self.extra_image_parts = set()

    def __call__(self):
        if not self.images or not self.labels:
            print("ERROR: No images or labels where found, cannot generate no match.")
            return

        self.images = [os.path.basename(image) for image in self.images]

        # print(len(self.images))
        # lent = len(self.images)
        # print(sorted(self.images)[lent-20:])

        image_parts = [self.get_part_name_with_suspicious(img) for img in self.images]
        label_parts = [self.get_part_name(label) for label in self.labels]

        image_parts = self.list_to_dict_sum(image_parts)
        label_parts = self.list_to_dict_sum(label_parts)

        print(f'LABELS originate from {len(label_parts)} parts.')
        print(f'IMAGES originate from {len(label_parts)} parts.')

        self.get_stats_about_parts(image_parts, label_parts)

        sus_img_parts = self.get_sus_parts(self.images)
        # print(f'\t{len(sus_img_parts)} part(s) has generated suspicious images.')
        logging.debug(f'sus parts: {sus_img_parts}')

        logging.debug('---- Finding complete parts: ----')
        logging.debug('----(printing only incomplete)---')
        complete_parts = self.get_complete_parts(image_parts, label_parts, sus_img_parts)

        self.print_results(complete_parts, sus_img_parts)
        # , copying to {self.output_folder}')

        # for i, file in enumerate(self.input_files):
        #     if not self.verbose:
        #         Common.print_dots(i, 200, 8_000)
        #     logging.debug('Working with: %d, %s', i, file)


        # self.print_results()
    def print_results(self, complete_parts, sus_img_parts):
        print('')
        print('--------------------------------------')
        print('Results:')
        total_parts_found_len = len(self.total_parts_found)
        print(f'From total {total_parts_found_len} unique parts found:')

        complete_ratio = len(complete_parts) / total_parts_found_len * 100
        sum_values = sum(complete_parts.values())
        print(f'\t{len(complete_parts)} ({complete_ratio:.1f} %) complete parts with '
              f'{sum_values} images and labels.')
        sus_ratio = len(sus_img_parts) / total_parts_found_len * 100
        print(f'\t{len(sus_img_parts)} ({sus_ratio:.1f} %) parts generated suspicious images.')

        not_fit_ratio = self.not_fitting_staff_count / total_parts_found_len * 100
        print(f'\t{self.not_fitting_staff_count} ({not_fit_ratio:.1f} %) parts '
              'had differenct counts of labels and images.')

        extra_image_parts_len = len(self.extra_image_parts)
        extra_image_ratio = extra_image_parts_len / total_parts_found_len * 100
        print(f'\t{extra_image_parts_len} ({extra_image_ratio:.1f} %) parts generated only images.')

        extra_label_parts_len = len(self.extra_label_parts)
        extra_label_ratio = extra_label_parts_len / total_parts_found_len * 100
        print(f'\t{extra_label_parts_len} ({extra_label_ratio:.1f} %) parts generated only labels.')


    def get_stats_about_parts(self, image_parts: dict, label_parts: dict) -> None:
        """Get stats about parts using dictionary input with names as keys. Save stats to self."""
        image_parts = set(image_parts.keys())
        label_parts = set(label_parts.keys())

        self.total_parts_found = image_parts.union(label_parts)
        self.extra_label_parts = label_parts - image_parts
        self.extra_image_parts = image_parts - label_parts


    def get_complete_parts(self, image_parts: dict, label_parts: dict, sus_img_parts: set):
        """Go through images dictionary and labels dictionary and return complete parts.

        Part is complete when the number of images is equal to the number of labels and 
        part has not generated any suspicious images."""
        complete_parts = {}

        for part_name, _ in image_parts.items():
            if (part_name in label_parts and
                    not part_name in sus_img_parts):
                if label_parts[part_name] == image_parts[part_name]:
                    # logging.debug(f'{part_name}:\t(i: {image_parts[part_name]},'
                    #               f' l: {label_parts[part_name]})\tOK')
                    complete_parts[part_name] = label_parts[part_name]
                else:
                    self.not_fitting_staff_count += 1
                    logging.debug(f'{part_name}:\t(i: {image_parts[part_name]},'
                                  f' l: {label_parts[part_name]})\t')

        return complete_parts

    def load_labels(self, filename: str) -> dict:
        """Load labels from file and return as a dictionary."""
        # print(f'labels file: {filename}')
        # print(f'path exists: {os.path.exists(filename)}')
        labels = Common.read_file(filename)

        if not labels:
            return {}

        labels_list = re.split(r'\n', labels)
        labels_list = list(filter(None, labels_list))   # filter out empty lines

        # print(type(labels_list))
        # print('len(labels_list): ')
        # print(len(labels_list))
        # print(labels_list[:10])

        labels = {}
        for label in labels_list:
            system_id, *sequence = re.split(r'\s', label)
            labels[system_id] = ' '.join(sequence)

        return labels

    def get_sus_parts(self, images: list) -> set:
        """Get a list of images in input folders, return onlysuspicious images.
        
        Suspicious image name starts with 'z'."""
        # print(images)
        # all_images = [os.path.basename(image) for image in self.images]

        sus_parts = set()
        for image in images:
            if image[0] == 'z':
                _, file_name, part_name, *_  = re.split(r'\_|\-', image)
                sus_parts.update(['_'.join([file_name, part_name])])

        return sus_parts


    def get_part_name(self, file: str):
        """Get file name, return part name."""
        mscz_id, part_id, *_ = re.split(r'_|-', file)
        # print(f'mscz: {mscz_id}, part: {part_id}, rest: {rest}')

        return f'{mscz_id}_{part_id}'

    def get_part_name_with_suspicious(self, file: str):
        """Get file name, return part name."""
        if file[0] == 'z':
            _, mscz_id, part_id, *_ = re.split(r'_|-', file)
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
        "-i", "--image-folder", default='.',
        help="Input folder where to look for images and sub-folders with images.")
    parser.add_argument(
        "-l", "--label-files", nargs='+',
        help="Files with labels.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='pairs',
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
        image_folder=args.image_folder,
        label_files=args.label_files,
        output_folder=args.output_folder,
        verbose=args.verbose)
    cutter()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
