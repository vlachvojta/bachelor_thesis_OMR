#!/usr/bin/python3.8

import argparse
import re
import sys
import os
from common import Common
import time
import symbol_converter


class Files_copier:

    file_names = []
    file_groups = []
    file_translator = {}
    exts = []
    output = ''
    max_img = [0, 0]
    height = 0
    width = 0

    def __init__(self, exts: list = ['semantic', 'agnostic', 'png'],
                 folders: list = ['.'],
                 output: str = 'output_folder',
                 height: int = 0,
                 width: int = 0) -> None:
        print('FC: Hello from FILES_COPIER (FC)')
        self.output = output
        self.exts = exts
        self.height = height
        self.width = width

        if not os.path.exists(output):
            os.mkdir(output)

        files = []
        for folder in folders:
            files += Common.get_files(folder, exts)

        files = list(set(files))
        self.file_names = Common.check_existing_files(files)

        print(f'Found {len(self.file_names)} files with one of '
              f'{len(exts)} extensions.')

        self.file_groups = Common.get_complete_group_names(self.file_names,
                                                           exts)

        print(f'Found {len(self.file_groups)} complete file groups ')
        diff = len(self.file_names) - (len(self.file_groups) * len(exts))
        if diff > 0:
            print(f'\t{diff} files are in incomplete group.')
        print(f'(every dot is 1000 parsed files.)')

        self.max_img = self.get_max_img_resolution(self.file_groups)
        print(f'FC: MAX_res: {self.max_img}')

        for i, file_group in enumerate(self.file_groups):
            self.write_group(file_group, i)
            self.file_translator.update({f'{i:06}': file_group})
            if i % 1000 == 0:
                print('.', end='')
                sys.stdout.flush()
        print('')

        file_translator_path = os.path.join(output, '0_file_translator.json')
        Common.save_dict_as_json(self.file_translator, file_translator_path)
        print(f'Dictionary with filenames written to: {file_translator_path}')

    def write_group(self, file_group: str = '', i: int = 0) -> None:
        """Get file group name, save it to output folder with every given ext

        File group name is file name without extension but with full path
        """
        for ext in self.exts:
            input_file = f'{file_group}.{ext}'
            output_file = os.path.join(self.output, f'{i:06}.{ext}')

            if re.match(r'jpg|png', ext):
                self.write_img(input_file, output_file)
            else:
                data = Common.read_file(input_file)
                # Convert text data here if needed
                Common.write_to_file(data, output_file)

    def write_img(self, input_file: str, output_file: str) -> None:
        data = Common.read_file(input_file)
        img_res = data.shape[0:2]
        assert img_res[0] <= self.max_img[0]
        assert img_res[1] <= self.max_img[1]

        if (img_res[0] < self.max_img[0] or
                img_res[1] < self.max_img[1]):

            data = Common.resize_img(data, self.height, self.width)

            # ? resize all images to match max_img height but keep ratio
            # data = Common.resize_img(data, self.max_img[0])

            # ? Add padding to both top and bottom
            # data = Common.add_black_border(data, self.max_img[0], 0)

            # ? For padding width of images do this instead of the line above
            # data = Common.add_black_border(data,
            #                                self.max_img[0],
            #                                self.max_img[1])

        Common.write_to_file(data, output_file)

    def get_max_img_resolution(self, file_groups: list = []) -> list:
        """Every file in list, add img extension, open with `cv2`, find max.

        Return max resolution found in format: `[height, width]`
        """
        max_height = 0
        max_width = 0
        exts = [e for e in self.exts if re.fullmatch(r'png|jpg', e)]

        for file_group in file_groups:
            for ext in exts:
                file_name = f'{file_group}.{ext}'
                height, width = Common.get_img_resolution(file_name)

                max_height = height if height > max_height else max_height
                max_width = width if width > max_width else max_width

        return [max_height, max_width]


def parseargs():
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-f", "--files", nargs='*', default=[],
    #     help=("Files to read symbols from, you can add more files\n" +
    #           "or use bash regex expr.\n" +
    #           "USE FULL FILE PATH (relative or absolute)"))
    parser.add_argument(
        "-e", "--extensions", nargs='*',
        default=['semantic', 'agnostic', 'png'],
        help=("Set file extensions for files in given folder\n" +
              "Use in combination with --directories."))
    parser.add_argument(
        "-F", "--src_folders", nargs='*', default=['.'],
        help=("Directories where to look for files with given extensions. \n" +
              "Use in combination with --extensions."))
    parser.add_argument(
        "-o", "--output_folder", default='output_folder',
        help="Set output file with extension. Output format is JSON")
    parser.add_argument(
        "-H", "--image_height", default='100', type=int,
        help=("Set to resize all images to given height." +
              "If not set and weigth is, keep ratio."))
    parser.add_argument(
        "-W", "--image_width", default='0', type=int,
        help=("Set to resize all images to given width." +
              "If not set and height is, keep ratio."))
    # parser.add_argument(
    #     "-c", "--copy_names", action="store_true", default='False',
    #     help="Set output file with extension. Output format is JSON")
    # parser.add_argument(
    #     "-i", "--input_file", default="files.txt",
    #     help="File with list of all files to search through.")
    # parser.add_argument(
    #     "-o", "--out", default='',
    #     help="Set output file, stdout by default")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    # fc = Files_copier(
    Files_copier(
        exts=args.extensions,
        folders=args.src_folders,
        output=args.output_folder,
        height=args.image_height,
        width=args.image_width)
    # database=args.database,
    # dirs=args.directories,
    # exts=args.extensions)

    # gus.finalize(args.output)
    # gus.print_symbols(args.out)

    end = time.time()
    print(f'Total time: {end - start}')


if __name__ == "__main__":
    main()
