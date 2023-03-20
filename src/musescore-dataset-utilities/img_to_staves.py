#!/usr/bin/python3.8
"""Separate images to individual music staves with very little white space arround.

Usage:
$ python3 img_to_staves.py -i image.png -o out/
resulting in creating cropped files out/image_s00.png, out/image_s01.png etc.
"""

import argparse
import re
import sys
import os
import time
import logging
import cProfile  # Profiling
import pstats  # Profiling

import numpy as np
# from PIL import Image
import cv2 as cv
# from matplotlib import pyplot as plt

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class StaffCuter:
    """Separate images to individual music staves with very little white space arround."""
    def __init__(self, input_files: list = None, input_folder: str = None,
                 output_folder: str = 'out', image_height: int = 100,
                 verbose: bool = False):
        self.input_files = input_files
        self.output_folder = output_folder
        self.image_height = image_height
        self.verbose = verbose

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
        for i, file in enumerate(self.input_files):
            if i % 1000 == 0:
                suspicious_files_path = os.path.join(self.output_folder, '0_suspicious_files.json')
                print(f'\t{len(self.suspicious_files)} files was suspicious, writing to file.')
                Common.write_to_file(self.suspicious_files, suspicious_files_path)
            if not self.verbose:
                Common.print_dots(i, 200, 8_000)
            logging.debug('Working with: %d, %s', i, file)
            image = cv.imread(file, cv.IMREAD_UNCHANGED)
            # image = Image.open(file)
            # image = np.asarray(image)
            logging.debug('\tImage opened')
            data = self.grayscale(image)
            logging.debug('\tgot Grayscale picture.')

            # # Calculate means of each row
            # means = []
            # for line in data:
            #     means.append(np.mean(line))

            # plt.plot(means)
            # plt.savefig('chart_mean.png')

            # staves = self.get_staves(data)
            staves = self.get_staves_new(data)
            logging.debug('\tgot %d staves', len(staves))

            cropped_staves = []
            for i, staff in enumerate(staves):
                # cropped_staves = self.get_staves_new(data.T)
                # # print(f'len(cropped_staves): {len(cropped_staves)}')
                # if len(cropped_staves) > 1:
                #     print(f'TOO much cut staves: {len(cropped_staves)}')
                # cropped_staff = cropped_staves[0].T
                # print(f'before: {staff.shape}, after: {cropped_staff.shape}')
                # Common.write_to_file(staff, os.path.join(self.output_folder, f'error_png_{i}.png'))
                logging.debug(f'\t\tcropping {i}')
                cropped_staff = self.crop_white_space(staff.T, strip_count=20).T

                # Delete everything that has too short lentgh (page numbers, labels, etc)
                too_narrow_image_threshold = 200
                if cropped_staff.shape[1] > too_narrow_image_threshold:
                    cropped_staves.append(cropped_staff)

            logging.debug('\tSeparated into %d staff images.', len(cropped_staves))

            for i, staff in enumerate(cropped_staves):
                # logging.debug(staff.shape)
                suspicious_threshold = 500
                logging.debug(f'\t{file}_s{i:02}.png: {staff.shape}')

                if staff.shape[0] > suspicious_threshold:
                    # image = Image.fromarray(staff)
                    base_file = os.path.basename(file)
                    self.suspicious_files.append(base_file)
                    self.save_image(staff, f'z_{base_file}', i)

                else:
                    staff = Common.resize_img(staff, self.image_height)
                    # image = Image.fromarray(staff)
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
        # logging.debug(f'file_name: {file_name}')
        file_name_parts = re.split(r'\.', os.path.basename(file_name))
        file_name = '.'.join(file_name_parts[:-1]) + f'_s{staff_number:02}.png'
        file_name_path = os.path.join(self.output_folder, file_name)
        # logging.debug(f'saving to: {file_name_path}')
        Common.write_to_file(image, file_name_path)
        # image = Image.fromarray(image)
        # image.save(file_name_path)
        self.generated_staves += 1

    def grayscale(self, image: np.ndarray):
        """Convert image to grayscale and return as numpy array.
        
        Check if values are stored in RGB values or just in ALPHA values."""
        # start_mean = time.time()
        means = []
        for i in range(4):
            means.append(np.mean(image[0,:,i]))
        # end_mean = time.time()
        # print(f'Mean counting time: {end_mean - start_mean:.5f} s')

        logging.debug(f'\tmeans: {means}')

        if sum(means[:3]) < 0.0001:
            # print('Image is only ALPHA')
            # Image data is only in ALPHA channel
            return 255 - image[:,:,3]
        # print('Image is NOT')
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    def get_staves_new(self, data) -> list:
        """Cut individual staves from img. Return in a list of staves."""
        # def strip_is_white(strip: np.ndarray()) -> bool:
        #     strip_min = np.min(strip)
        #     return strip_min > line_min_threshold

        lines_in_strip = 5
        line_min_threshold = 249

        # Round image size to the nearest multiple of lines_in_group
        max_height = (data.shape[0] // lines_in_strip) * lines_in_strip
        data = data[:max_height]
        # print(f'data.shape: {data.shape}')
        data_strips = data.reshape([-1,lines_in_strip,data.shape[1]])
        # print(f'data_strips.shape: {data_strips.shape}')

        white_strip_indexes = [[0]]

        for strip_i, strip in enumerate(data_strips, 1):
            strip_min = np.min(strip)

            strip_is_white = strip_min > line_min_threshold
            # print(f'{strip_i}, np.min(strip): {strip_min}, strip_is_white: {strip_is_white}')
            if strip_is_white:
                # back_strip = data_strips[strip_i-2: strip_i]
                # if back_strip.shape[0] == 0:
                #     continue
                # back_strip_min = np.min(back_strip)
                # print(f'strip_i: {strip_i}, white_strip_indexes[-1]: {white_strip_indexes[-1]}')
                previous_strip_is_white = (strip_i-1 == white_strip_indexes[-1][-1])
                if previous_strip_is_white:
                    # print('previous_strip_is_white')
                    white_strip_indexes[-1].append(strip_i)
                else:
                    # if white_strip_indexes == []:
                    #     white_strip_indexes.append([strip_i])
                    # else:
                    white_strip_indexes.append([strip_i])
                    # logging.debug(f'Staves[-1].shape: {staves[-1].shape}')

        # print(white_strip_indexes)
        # print(f'len(white_strip_indexes): {len(white_strip_indexes)}')

        staves = []
        for white_strip_i in range(len(white_strip_indexes) - 1):
            staff_start = white_strip_indexes[white_strip_i][-1] * lines_in_strip
            staff_end = white_strip_indexes[white_strip_i + 1][0] * lines_in_strip
            staves.append(data[staff_start:staff_end])

        staves = self.add_border(staves)

        return staves

    def get_staves(self, data) -> list:
        """Cut individual staves from img. Return in a list of staves."""
        staves = []
        line_mean_threshold = 250

        # logging.debug(data.shape)

        for i, line in enumerate(data[1:]):
            if self.verbose and i % 500 == 0:
                logging.debug(f'\t\ti: {i}, len(line): {len(staves)}')
            # if i < 20: logging.debug(f'{i}: np.min(line): {np.min(line)}')
            # if i % 50 == 0: logging.debug(f'i: {i}, len(staves): {len(staves)}')
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
                        # logging.debug(f'Staves[-1].shape: {staves[-1].shape}')

        staves = self.add_border(staves)

        return staves

    def add_border(self, staves:list, height: int=20) -> list:
        border_width = max([stave.shape[1] for stave in staves])
        border = np.zeros((height, border_width), dtype='uint8') + 255

        new_staves = []

        for staff in staves:
            if staff.shape[0] > 20:
                new_staves.append(np.concatenate((border, staff, border), axis=0))
        return new_staves

    def crop_white_space(self, data: np.ndarray,
                   strip_count: int = 5) -> np.ndarray:
        """Crop image iteratively and stop when it finds the staff."""
        safety_threshold = 3
        for _ in range(safety_threshold):
            cropped_data = 'empty'

            strip_height = max(len(data) // strip_count, 1)
            # logging.debug(f'len(data): {len(data)}, strip_count: {strip_count}, '
            #       f'strip_height: {strip_height}')

            for i in range(strip_count):
                strip = data[(strip_height * i) : (strip_height * (i + 1))]
                # logging.debug(f'i: {i}, data.shape: {data.shape}, strip.shape: {strip.shape}')
                # logging.debug(f'strip_height: {strip_height}')
                # logging.debug(strip)

                # check if strip is not too thin
                min_width_threshold = 20
                if strip.shape[0] < min_width_threshold:
                    return strip

                if np.min(strip) == 0:
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
        help="Image height in px to resize all images to. If -1, height will be left unchanged.")
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
    parser.add_argument(  # Profiling
        "-p", "--profile-output", type=str, default='profile_dump.prof',
        help="File to output profiling results.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    with cProfile.Profile() as profile:  # Profiling
        cutter = StaffCuter(
            input_files=args.input_files,
            input_folder=args.input_folder,
            output_folder=args.output_folder,
            image_height=args.image_height,
            verbose=args.verbose)
        cutter()

    # Profiling
    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    # results.print_stats()
    results.dump_stats(args.profile_output)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
