#!/usr/bin/python3.8
"""Separate images to individual music staves with very little white space arround.

2 modes of splitting staves:
    Naive mode: Uses white space horizontal strips to recognize space between staves
    Informed mode: Needs n staff count, cuts whitespace horizontal strips
        and then divides the rest to n individual staves.

Usage:
$ python3 img_to_staves.py -i image.png -o out/
resulting in creating cropped files out/image_s00.png, out/image_s01.png etc.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import argparse
import re
import sys
import os
import time
import logging
from enum import Enum

import numpy as np
import cv2 as cv

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class Mode(Enum):
    """Class for splitting mode of StaffCuter"""
    INFORMED = 1
    NAIVE = 2


class StaffCuter:
    """Separate images to individual music staves with very little white space arround."""
    def __init__(self, input_files: list = None, input_folder: str = None,
                 output_folder: str = 'out', image_height: int = 100, staff_count: int = None,
                 verbose: bool = False):
        self.input_files = input_files
        self.output_folder = output_folder
        self.image_height = image_height
        self.verbose = verbose
        self.mode = Mode.NAIVE if staff_count is None else Mode.INFORMED
        self.staff_count = staff_count

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO,format='[%(levelname)-s]\t- %(message)s')

        if not input_folder is None:
            listdir = os.listdir(input_folder)
            if not input_files:
                input_files = [os.path.join(input_folder, file) for file in listdir]
            else:
                input_files = input_files + [os.path.join(input_folder, file) for file in listdir]

        self.input_files = Common.check_files(input_files, ['png'])
        if not self.input_files:
            print('No valid input files provided.')

        print(f'Found {len(self.input_files)} input files.')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.suspicious_files = []
        self.generated_staves = 0

    def __call__(self):
        if not self.verbose:
            print(f'Going through {len(self.input_files)} input files, separating to staves. '
                  '(every dot is 200 files, every line is 1_000)')

        for i, file in enumerate(self.input_files):
            if i > 0 and i % 1000 == 0:
                suspicious_files_path = os.path.join(self.output_folder, '0_suspicious_files.json')
                print(f'\t{len(self.suspicious_files)} files was suspicious, writing to file.')
                Common.write_to_file(self.suspicious_files, suspicious_files_path)
            if not self.verbose:
                Common.print_dots(i, 200, 1_000)
            logging.debug('Working with: %d, %s', i, file)
            image = cv.imread(file, cv.IMREAD_UNCHANGED)
            data = self.grayscale(image)
            logging.debug('\tgot Grayscale picture.')


            if self.mode == Mode.NAIVE:
                staves = self.get_staves_naive(data)
            elif self.mode == Mode.INFORMED:
                staves = self.get_staves_informed(data, self.staff_count)

            logging.debug('\tgot %d staves', len(staves))

            cropped_staves = []
            for i, staff in enumerate(staves):
                # Crop horizontal white space
                cropped_staff = self.crop_white_space(staff.T, strip_count=20).T

                # Delete everything that has too short lentgh (page numbers, labels, etc)
                too_narrow_image_threshold = 200
                if cropped_staff.shape[1] > too_narrow_image_threshold:
                    cropped_staves.append(cropped_staff)

            logging.debug('\tSeparated into %d staff images.', len(cropped_staves))

            for i, staff in enumerate(cropped_staves):
                suspicious_threshold = 500
                logging.debug(f'\t{file}_s{i:02}.png: {staff.shape}')

                if self.mode == Mode.NAIVE and staff.shape[0] > suspicious_threshold:
                    base_file = os.path.basename(file)
                    self.suspicious_files.append(base_file)
                    self.save_image(staff, f'z_{base_file}', i)

                else:
                    staff = Common.resize_img(staff, self.image_height)
                    self.save_image(staff, file, i)

        self.print_results()

    def print_results(self):
        """Print stats for input and output files."""
        print('')
        print('--------------------------------------')
        print('Results:')
        print(f'From {len(self.input_files)} input files:')
        print(f'\t{self.generated_staves} generated staves.')

        if len(self.suspicious_files) > 0:
            self.suspicious_files = sorted(list(set(self.suspicious_files)))
            print(f'\t{len(self.suspicious_files)} files was suspicious.')
            suspicious_files_path = os.path.join(self.output_folder, '0_suspicous_files.json')

            if not os.path.exists(suspicious_files_path):
                Common.write_to_file(self.suspicious_files, suspicious_files_path)
            else:
                # TODO concat existing file to new and save
                print(f'WARNING: {suspicious_files_path} already exists, '
                      'printing to stdout instead')
                print(self.suspicious_files)

    def save_image(self, image: np.ndarray, file_name: str, staff_number: int):
        """Save image."""
        file_name_parts = re.split(r'\.', os.path.basename(file_name))
        file_name = '.'.join(file_name_parts[:-1]) + f'_s{staff_number:02}.png'
        file_name_path = os.path.join(self.output_folder, file_name)
        logging.debug(f'saving to: {file_name_path}')
        Common.write_to_file(image, file_name_path)
        self.generated_staves += 1

    def grayscale(self, image: np.ndarray):
        """Convert image to grayscale and return as numpy array.
        
        Check if values are stored in RGB values or just in ALPHA values."""
        means = []
        for i in range(4):
            means.append(np.mean(image[0,:,i]))

        logging.debug(f'\tmeans: {means}')

        if sum(means[:3]) < 0.0001:
            # Image data is only in ALPHA channel
            return 255 - image[:,:,3]
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    def get_staves_informed(self, data, staff_count: int = 1) -> list:
        """Cut individual staves from img. Return in a list of staves. Use Informed mode.
        
        Informed mode: Needs staff count n, cuts whitespace horizontal strips
            and then divides the rest to n individual staves.
        """
        division_margin_percent = 0.25

        # crop white space of whole page
        data = self.crop_white_space(data, strip_count=40, safety_threshold=1)

        if staff_count <= 1:
            staves = [data]
        else:
            # get division points
            strip_width = data.shape[0] // staff_count
            division_margin = int(strip_width * division_margin_percent)

            division_points = [strip_width * i for i in range(staff_count)] + [data.shape[0]]

            # divide to staves WITH MARGIN over the division points
            staves = []
            for i, division_point in enumerate(division_points[:-1]):
                staff_start = max(0, division_point - division_margin)
                staff_end = min(division_points[i + 1] + division_margin, division_points[-1])
                staves.append(data[staff_start:staff_end])

        # crop white space of every staff and add border to every stave
        staves_out = []
        for staff in staves:
            staves_out.append(self.crop_white_space(staff, strip_count=20, safety_threshold=1))

        staves_out = self.add_border(staves_out)
        logging.debug(f'\tReturning {len(staves_out)} staves')
        return staves_out

    def get_staves_naive(self, data) -> list:
        """Cut individual staves from img. Return in a list of staves. Use Naive mode.
        
        Naive mode uses white space horizontal strips to recognize space between staves.
        """
        lines_in_strip = 5
        line_min_threshold = 249

        # Round image size to the nearest multiple of lines_in_group
        max_height = (data.shape[0] // lines_in_strip) * lines_in_strip
        data = data[:max_height]
        data_strips = data.reshape([-1,lines_in_strip,data.shape[1]])

        white_strip_indexes = [[0]]

        for strip_i, strip in enumerate(data_strips, 1):
            strip_min = np.min(strip)

            strip_is_white = strip_min > line_min_threshold
            if strip_is_white:
                previous_strip_is_white = strip_i-1 == white_strip_indexes[-1][-1]
                if previous_strip_is_white:
                    white_strip_indexes[-1].append(strip_i)
                else:
                    white_strip_indexes.append([strip_i])

        staves = []
        for white_strip_i in range(len(white_strip_indexes) - 1):
            staff_start = white_strip_indexes[white_strip_i][-1] * lines_in_strip
            staff_end = white_strip_indexes[white_strip_i + 1][0] * lines_in_strip
            staves.append(data[staff_start:staff_end])

        staves = self.add_border(staves)

        return staves

    def get_staves(self, data) -> list:
        """Cut individual staves from img. Return in a list of staves. 

        This metoed is DEPRICATED. use `get_staves_naive` or `get_staves_informed`!
        """
        staves = []
        line_mean_threshold = 250


        for i, line in enumerate(data[1:]):
            if self.verbose and i % 500 == 0:
                logging.debug(f'\t\ti: {i}, len(line): {len(staves)}')
            if np.min(line) < line_mean_threshold:
                strip = data[i-20 : i]
                if strip.shape[0] == 0:
                    continue
                strip_min = np.min(strip)
                if strip_min > line_mean_threshold:
                    staves.append(np.array([line]))
                elif strip_min < line_mean_threshold:
                    if not staves:
                        staves.append(np.array([line]))
                    else:
                        staves[-1] = np.concatenate((staves[-1], [line]), axis=0)

        staves = self.add_border(staves)

        return staves

    def add_border(self, staves:list, height: int=20) -> list:
        border_width = max([staff.shape[1] for staff in staves])
        border = np.zeros((height, border_width), dtype='uint8') + 255

        new_staves = []

        for staff in staves:
            if staff.shape[0] > 10:
                new_staves.append(np.concatenate((border, staff, border), axis=0))
        return new_staves

    def crop_white_space(self, data: np.ndarray, strip_count: int = 5,
                         safety_threshold: int = 3) -> np.ndarray:
        """Crop image iteratively and stop when it finds the staff.
        
        Crop horizontal white_space strips.
        """
        for _ in range(safety_threshold):
            cropped_data = 'empty'

            strip_height = max(len(data) // strip_count, 1)

            for i in range(strip_count):
                strip = data[(strip_height * i) : (strip_height * (i + 1))]

                # check if strip is not too thin
                min_width_threshold = 20
                if strip.shape[0] < min_width_threshold:
                    return data

                strip_is_not_white_space = np.min(strip) == 0
                if strip_is_not_white_space:
                    if isinstance(cropped_data, str):
                        cropped_data = strip
                    else:
                        cropped_data = np.append(cropped_data, strip, axis=0)

            if cropped_data.shape == data.shape:
                break
            data = cropped_data

        return data


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-I", "--input-files", nargs='*', default=None,
        help="Input images to cut.")
    parser.add_argument(
        "-i", "--input-folder", type=str, default=None,
        help="Input folder where to look for images to cut.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='out',
        help="Output folder to write cut imgs to.")
    parser.add_argument(
        "--image-height", type=int, default=100,
        help="Image height in px to resize all images to.")
    parser.add_argument(
        "-s", "--staff-count", type=int, default=None,
        help=("If None, do naive splitting, "
              "else split to this number of staves using 'informed' algorithm."))
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    cutter = StaffCuter(
        input_files=args.input_files,
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        image_height=args.image_height,
        staff_count=args.staff_count,
        verbose=args.verbose)
    cutter()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
