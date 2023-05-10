#!/usr/bin/python3.8

import argparse
import re
import sys
import os
from common import Common
import time
from symbol_converter import Symbol_converter
import shutil
import pandas as pd


class Files_copier:

    # arguments
    exts = []
    file_names = []
    output = ''
    height = 0
    width = 0
    update_files = False
    convert_symbols = False

    file_groups = []
    file_groups_img_widths = {}
    file_translator = {}
    max_img = [0, 0]
    FILE_TRANSLATOR_NAME = '0_file_translator.json'
    FILE_TRANSLATOR_PATH = ''

    sc = None   # symbol_converter instance

    def __init__(self, exts: list = ['agnostic', 'semantic', 'png'],
                 folders: list = ['.'], output: str = 'output_folder',
                 height: int = 0, width: int = 0, update_files: bool = False, 
                 convert_symbols: bool = False) -> None:
        print('FC: Hello from FILES_COPIER (FC)')
        self.output = output
        self.exts = exts
        self.height = height
        self.width = width
        self.update_files = update_files
        self.FILE_TRANSLATOR_PATH = os.path.join(
            output,
            self.FILE_TRANSLATOR_NAME)
        self.convert_symbols = convert_symbols

        old_file_translator = self.get_old_file_translator()

        if not os.path.exists(output):
            os.mkdir(output)

        self.file_groups = self.get_file_groups(folders, exts)

        print(f'Found {len(self.file_groups)} complete file groups ')
        diff = len(self.file_names) - (len(self.file_groups) * len(exts))
        if diff > 0:
            print(f'\t{diff} files are in incomplete group.')
        print(f'(every dot is 1000 parsed files.)')

        # print(f'Getting max img resolution...')
        # self.max_img = self.get_max_img_resolution(self.file_groups)
        # print(f'MAX_res: {self.max_img}')

        self.check_fgroups_identcal(old_file_translator.values(),
                                    self.file_groups)

        print(f'After sort, there is {len(self.file_groups)} '
              f'file_groups to convert')

        if self.convert_symbols:
            self.sc = Symbol_converter()

        if old_file_translator == {}:
            file_translator = {i: fgroup for i, fgroup
                               in enumerate(self.file_groups)}
            self.write_all_groups(file_translator)
        else:
            self.write_all_groups({int(k): v for k, v
                                  in old_file_translator.items()})

        Common.save_dict_as_json(self.file_translator,
                                 self.FILE_TRANSLATOR_PATH)
        print(f'Dictionary with filenames written to: '
              f'{self.FILE_TRANSLATOR_PATH}')

    def write_all_groups(self, keys_fgroups: dict) -> None:
        for i, file_group in keys_fgroups.items():
            Common.print_dots(i)
            self.write_group(file_group, i)
            self.file_translator.update({f'{i:06}': file_group})
        print('')

    def write_group(self, file_group: str = '', i: int = 0) -> None:
        """Get file group name, save it to output folder with every given ext

        File group name is file name without extension but with full path
        """
        for ext in self.exts:
            input_file = f'{file_group}.{ext}'
            output_file = os.path.join(self.output, f'{i:06}.{ext}')

            if not self.update_files and os.path.exists(output_file):
                continue

            if re.match(r'jpg|png', ext):
                data = Common.read_file(input_file)
                output = self.write_img(data)
                Common.write_to_file(output, output_file)
            elif re.match(r'agnostic|semantic', ext):
                data = Common.read_file(input_file)
                if data is None:
                    print(input_file)
                if self.convert_symbols and self.sc is not None:
                    data = self.convert_symbols_function(data)
                Common.write_to_file(data, output_file)
            else:
                print(f'[Warning] File of unknown type: {ext}')
                shutil.copy(input_file, output_file)

    def write_img(self, data) -> None:
        img_res = data.shape[0:2]
        # assert img_res[0] <= self.max_img[0]
        # assert img_res[1] <= self.max_img[1]

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
        return data

    def check_fgroups_identcal(self, old, new) -> None:
        old = sorted(old)
        new = sorted(new)

        if not old == new:
            print('OLD != NEW')
            print(f'\tnew len: {len(old)}\n'
                  f'\told len: {len(new)}')
            raise AssertionError

    def get_old_file_translator(self):
        old_file_translator = {}
        if (os.path.exists(self.output) and
                os.path.exists(self.FILE_TRANSLATOR_PATH)):
            old_file_translator = Common.read_file(self.FILE_TRANSLATOR_PATH)
        return old_file_translator

    def get_file_groups(self, folders, exts) -> list:
        files = []
        for folder in folders:
            files += Common.get_files(folder, exts)

        files = list(set(files))
        self.file_names = Common.check_existing_files(files)

        print(f'Found {len(self.file_names)} files with one of '
              f'{len(exts)} extensions.')

        return Common.get_complete_group_names(self.file_names, exts)

    def convert_symbols_function(self, data: str) -> str:
        assert isinstance(data, str)

        symbols = re.split(r'\s', data)
        symbols = [s for s in symbols if s != '']

        converted_symbols = self.sc.convert_list(symbols)
        assert len(symbols) == len(converted_symbols)

        return ' '.join(converted_symbols)

    def get_max_img_resolution(self, file_groups: list = []) -> list:
        """Every file in list, add img extension, open with `cv2`, find max.

        Return max resolution found in format: `[height, width]`
        """
        max_height = 0
        max_width = 0
        exts = [e for e in self.exts if re.fullmatch(r'png|jpg', e)]
        if exts == []:
            return [0, 0]
        img_widths = []

        for i, file_group in enumerate(file_groups):
            Common.print_dots(i)
            for ext in exts:
                file_name = f'{file_group}.{ext}'
                height, width = Common.get_img_resolution(file_name)

                if self.height > 0 and self.width == 0:
                    # calculate width after resizing height
                    ratio = self.height / float(height)
                    out_width = int(width * ratio)

                    # save to dict (v: file_group, k: width afet)
                    img_widths.append(out_width)

                max_height = height if height > max_height else max_height
                max_width = width if width > max_width else max_width
        print('')

        df = pd.DataFrame({'file_groups': file_groups, 'widths': img_widths})
        df['widths'] = df['widths'].astype('category')
        df = df.sort_values(by='widths', ascending=True).reset_index()
        self.file_groups = df['file_groups'].tolist()

        return [max_height, max_width]


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e", "--extensions", nargs='*',
        default=['agnostic', 'semantic'],  # TODO return to default ['agnostic', 'semantic', 'png']
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
    parser.add_argument(
        "-u", "--update_files", default=False, action='store_true',
        help=("Set true to update existin files in output_folder with "
              "new files from src_folder"))
    parser.add_argument(
        "-c", "--convert-symbols", default=False, action='store_true',
        help=("Set true to convert symbols to shorter form using "
              "symbol_converter module"))
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    Files_copier(
        exts=args.extensions,
        folders=args.src_folders,
        output=args.output_folder,
        height=args.image_height,
        width=args.image_width,
        update_files=args.update_files,
        convert_symbols=args.convert_symbols)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
