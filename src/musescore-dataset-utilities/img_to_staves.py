#!/usr/bin/python3.8
"""Separate images to individual music staves with very little white space arround.

Usage:
$ python3 img_to_staves.py -i image.png -o out/
resulting in creating cropped files out/image_s000.png, out/image_s001.png etc.
"""

import argparse
import re
import sys
import os
import time
import numpy as np
from PIL import Image, ImageOps


rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class StaffCuter:
    """Separate images to individual music staves with very little white space arround."""
    def __init__(self, input_files: list, output_folder: str = '.',
                 image_height: int = 100):
        self.output_folder = output_folder
        self.input_files = input_files
        self.image_height = image_height

        self.input_files = Common.check_existing_files(input_files)
        if not self.input_files:
            raise ValueError('No valid input files provided.')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def __call__(self):
        for file in self.input_files:
            print(f'Working with: {file}')
            image = Image.open(file)
            image = ImageOps.grayscale(image)
            data = np.asarray(image)

            staves = self.get_staves(data)

            print(f'\tSeparated into {len(staves)} staff images.')

            for i, staff in enumerate(staves):
                cropped_staff = self.crop_white_space(staff.T, strip_count=20).T

                # TODO resize image according to self.height HERE

                image = Image.fromarray(cropped_staff)

                self.save_image(image, file, i)

    def save_image(self, image: Image, file_name: str, staff_number: int):
        """Save image."""
        file_name_parts = re.split(r'\.', os.path.basename(file_name))
        file_name = '.'.join(file_name_parts[:-1]) + f'_s{staff_number:03}.png'
        file_name_path = os.path.join(self.output_folder, file_name)
        image.save(file_name_path)

    def get_staves(self, data) -> list:
        """Cut individual staves from img. Return in a list of staves."""
        staves = []
        line_mean_threshold = 250

        for i, line in enumerate(data[1:]):
            if np.min(line) < line_mean_threshold:
                if np.min(data[i-20 : i]) > line_mean_threshold:
                    staves.append(np.array([line]))
                elif np.min(data[i-20 : i]) < line_mean_threshold:
                    if not staves:
                        staves.append(np.array([line]))
                    else:
                        staves[-1] = np.concatenate((staves[-1], [line]), axis=0)

        border = np.zeros((20, data.shape[1]), dtype='uint8') + 255

        new_staves = []

        for i, staff in enumerate(staves):
            if staff.shape[0] > 20:
                new_staves.append(np.concatenate((border, staff, border), axis=0))

        return new_staves

    def crop_white_space(self, data: np.ndarray,
                   strip_count: int = 5) -> np.ndarray:
        """Crop image iteratively and stop when it finds the staff."""
        safety_threshold = 10
        for _ in range(safety_threshold):
            cropped_data = 'empty'

            strip_height = len(data) // strip_count

            for i in range(strip_count):
                strip = data[(strip_height * i) : (strip_height * (i + 1))]

                if np.min(strip) == 0:
                    if isinstance(cropped_data, str):
                        cropped_data = strip
                    else:
                        cropped_data = np.append(cropped_data, strip, axis=0)

            if cropped_data.shape == data.shape:
                break
            else:
                data = cropped_data

        return data


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-files", nargs='+',   # ? change to -I ?
        help="Input images to cut.")
    # TODO implemet --input-folder
    parser.add_argument(
        "-o", "--output-folder", type=str, default='.',
        help="Output folder to write cut imgs to.")
    parser.add_argument(
        "--image-height", type=int, default=100,  # TODO: implement this option
        help="Image height in px to resize all images to. If -1, height will be left unchanged.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    cutter = StaffCuter(
        input_files=args.input_files,
        output_folder=args.output_folder,
        image_height=args.image_height)
    cutter()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
