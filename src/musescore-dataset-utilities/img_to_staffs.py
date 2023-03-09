#!/usr/bin/python3.8
"""Cut images to sperate music staffs.
Example run:
$ python3 evaluate_checkpoints.py --ground-truth data.tst \
        --checkpoint-folder checkpoints
"""

import argparse
import re
import sys
import os
import time
import numpy as np
# import matplotlib.pyplot as plt
# import cv2 as cv
from PIL import Image, ImageOps


rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class StaffCuter:
    """Cut images to sperate music staffs."""

    def __init__(self, input_files: list,
                 output_folder: str = '.',
                 staff_count: int = 1):
        self.output_folder = output_folder
        self.staff_count = staff_count

        if not staff_count == 1:
            print('WARNING: staff_count other then 1 is not supported YET.')

        self.input_files = Common.check_existing_files(input_files)
        if not input_files:
            raise ValueError('No valid input files provided.')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        print(f'Working with: {input_files[0]}')
        image = Image.open(self.input_files[0])
        image = ImageOps.grayscale(image)
        print(image.format)
        print(image.size)
        print(image.mode)
        print('--------------')
        data = np.asarray(image)

        ### plot means to chart
        # means = data[0:1500].mean(axis=1)
        # print(means.shape)
        # plt.plot(means)
        # plt.title('Means of DPI 250')
        # plt.savefig(os.path.join(output_folder, 'chart_of_means_DPI_250.png'))

        # Crop vertical white space
        cropped_data = self.crop_white_space(data, strip_count=10)

        # Crop Horizontal white space
        cropped_data = self.crop_white_space(cropped_data.T, strip_count=20).T

        image = Image.fromarray(cropped_data)

        # Save image from np array
        out_file = re.split(r'\.', os.path.basename(input_files[0]))[0] + f'_cropped.png'
        out_file = os.path.join(output_folder, out_file)
        image.save(out_file)
        print(f'Saved: {out_file}')

        # image.save(os.path.join(self.output_folder, os.path.basename(input_files[0])))

    def crop_horizontal(self, image: Image) -> Image:
        """Crop the image horizontally to reduce whitespace."""
        w, h = image.size
        crop_edge = 50

        if crop_edge * 2 > w:
            return image

        image = image.crop((crop_edge, 0, w - (crop_edge * 2 ), h))
        return image

    def crop_white_space(self, data: np.ndarray,
                   strip_count: int = 5) -> np.ndarray:
        """Crop image iteratively and stop when it finds the staff."""
        safety_threshold = 10
        for j in range(safety_threshold):
            print('------------')
            print(f'j: {j}')

            cropped_data = 'empty'

            strip_height = len(data) // strip_count
            print(f'strip_height: {strip_height}')

            for i in range(strip_count):
                print(f'i: {i}')
                strip = data[(strip_height * i) : (strip_height * (i + 1))]

                if np.min(strip) == 0:
                    if isinstance(cropped_data, str):
                        cropped_data = strip
                    else:
                        cropped_data = np.append(cropped_data, strip, axis=0)
                else:
                    print('cut cut.')

            print(cropped_data.shape)
            if cropped_data.shape == data.shape:
                break
            else:
                data = cropped_data

        return data


def parseargs():
    """Parse arguments."""
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-files", nargs='+',
        help="Input images to cut.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='.',
        help="Output folder to write cut imgs to.")
    parser.add_argument(
        "-n", "--staff-count", type=int, default=1,
        help="Indicates how many staffs to cut fro every image.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    StaffCuter(
        input_files=args.input_files,
        output_folder=args.output_folder,
        staff_count=args.staff_count)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
