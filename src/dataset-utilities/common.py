#!/usr/bin/python3.8


import pathlib
import re
import os
import sys
import json
import time
import cv2 as cv


class Common:
    """Class for common tasks with dataset."""

    @staticmethod
    def print_dict(data: dict, files: bool = False):
        """Print dictionary in a way I like.

        if files, print `data[files]` the first
        if sort, sort every list in `data.values()`
        """
        print('{')

        if files and 'files' in list(data.keys()):
            keys = sorted(list(data.keys()))
            keys.pop(keys.index('files'))
            print(keys)
            print(f'\tfiles: {data["files"]}')
        else:
            keys = sorted(list(data.keys()))
            print(keys)

        for key in keys:
            print(f'\t{key}:')
            print(f'\t\t{data[key]}')
        print('}')

    @staticmethod
    def check_existing_files(files: list = []):
        """Return only existing file"""
        def file_is_visible(file: str = '') -> bool:
            return re.split(os.sep, file)[-1][0] != '.'

        return [file for file in files
                if os.path.exists(file) and file_is_visible(file)]

    @staticmethod
    def get_existing_file_names(files, dirs, exts, recursive):
        """Get files, return only existing ones.

        Get file names from directory with given extension + files.
        """
        existing_files = [file for file in files if os.path.exists(file)]

        if not dirs:
            return existing_files

        print('for')
        for dir in dirs:
            print(dir)
            print(os.listdir(dir))

        return existing_files

    @staticmethod
    def save_dict_as_json(data: dict, file: str) -> None:
        with open(file, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def write_to_file(data, file) -> None:
        """Caller is responsible for what is sent to which type of file."""
        file_extension = file.split('.')[-1]

        if file_extension == 'json':
            with open(file, 'w') as f:
                json.dump(data, f)
        elif re.fullmatch(r'png|jpg', file_extension):
            cv.imwrite(file, data)
        else:
            with open(file, 'w') as f:
                f.write(data)

    @staticmethod
    def read_file(file: str):
        """Read file, if file extension == 'json', read as json"""
        if not os.path.exists(file):
            return

        file_extension = file.split('.')[-1]

        if file_extension == 'json':
            with open(file) as f:
                data = json.load(f)
        elif re.fullmatch(r'png|jpg', file_extension):
            data = cv.imread(file)
        else:
            with open(file) as f:
                data = f.read()
        return data

    @staticmethod
    def get_lines(file) -> list:
        data = Common.read_file(file)
        if data:
            return data.split('\n')
        else:
            return []

    @staticmethod
    def get_files(folder: str = '.', exts: list = ['semantic']) -> list:

        print(f'Looking for all files in {folder}')
        files = []
        dirs = []
        for f in Common.full_list(folder):
            if os.path.isdir(f):
                dirs.append(f)
            elif os.path.isfile(f) and Common.right_file_ext(f, exts):
                files.append(f)

        assert len(dirs) > 0

        if dirs:
            print(f'Looking for files in {len(dirs)} folders.\n'
                  f'(every dot is 1000 folders)')
            for i, dir in enumerate(dirs):
                if i % 1000 == 0:
                    print('.', end='')
                    sys.stdout.flush()
                # if i > 5000:
                #     break
                files += [
                    f for f in Common.full_list(dir)
                    if os.path.isfile(f) and Common.right_file_ext(f, exts)]
        print('')
        return files

    @staticmethod
    def full_list(folder):
        """Get listdir but every file has full (relative or absolute) path."""
        return [os.path.join(folder, f) for f in os.listdir(folder)]

    @staticmethod
    def right_file_ext(file: str, exts: list) -> bool:
        if not file:
            return False
        return file.split('.')[-1] in exts

    @staticmethod
    def sum_lists_in_dict(data: dict = {}) -> int:
        """Return sum of all unique symbols found."""
        sum = 0
        for v in data.values():
            sum += len(v)
        return sum

    @staticmethod
    def serialize_dict_to_list(data: dict = {}) -> list:
        return data.values()
        # result = []
        # for v in data.values():
        #     result += v
        # return result

    @staticmethod
    def get_complete_group_names(files: list = [], exts: list = []) -> list:
        """Get list of all files, check if for every file name
        all extensions are present.
        Return list of complete file groups."""
        def cut_ext(file: str = '') -> str:
            return '.'.join(re.split(r'\.', file)[:-1])

        def get_ext(file: str = '') -> str:
            return re.split(r'\.', file)[-1]

        # print('GET_COMPLETE_GROUPS_NAMES')
        # print('========================')

        files = sorted(files)
        file_groups = []

        for i, file in enumerate(files):
            # print(f'file: {file}')
            # if len(file_groups) > 0: print(file_groups[-1][0])
            # print(f'cut_ext: {cut_ext(file)}')
            # print(f'get_ext: {get_ext(file)}')

            if len(file_groups) > 0 and file_groups[-1][0] == cut_ext(file):
                file_groups[-1].append(get_ext(file))
                # print('appending new ext')
            else:
                file_groups.append([cut_ext(file), get_ext(file)])
                # print('appending new file')
        # print(file_groups)

        complete_file_groups = []
        for file_group in file_groups:
            if len(set(file_group[1:])) == len(exts):
                complete_file_groups.append(file_group[0])
            else:
                print(f'{file_group[0]} is incomplete, because {file_group}')
        # print('========================')
        # print(f'complete_file_groups: {complete_file_groups}')
        # print('========================')

        return complete_file_groups

    # ======================== Image stats and manipulation ==================

    @staticmethod
    def get_img_resolution(file_name: str) -> int:
        return cv.imread(file_name).shape[0:2]

    def add_black_border(img, new_height: int = 0, new_width: int = 0):
        """if new params are 0 or smaller than actual size, do nothing."""
        def calculate_border_sizes(in_res: int, new_res: int):
            """in_res is resolution of input image, new_res is parent param"""
            out_res = [0, 0]
            if new_res > in_res:
                border_res = (new_res - in_res)
                if border_res % 2 == 1:
                    out_res = [(border_res // 2) + 1, border_res // 2]
                else:
                    out_res = [(border_res // 2)] * 2
            return out_res

        BLACK = [0, 0, 0]

        in_res = img.shape[0:2]
        # border_height = new_height - in_res[0]
        out_heights = calculate_border_sizes(in_res[0], new_height)

        if new_width > in_res[1]:
            border_width = new_width - in_res[1]
        else:
            border_width = 0
        # out_widths = calculate_border_sizes(in_res[1], new_width)

        img = cv.copyMakeBorder(
            img, out_heights[0], out_heights[1],
            0, border_width,
            cv.BORDER_CONSTANT, value=BLACK)

        return img

    def resize_img(img, height=0, width=0, inter=cv.INTER_AREA):
        dim = (height, width)
        (h, w) = img.shape[:2]

        if width == 0 and height == 0:
            return img

        if width == 0:
            ratio = height / float(h)
            dim = (int(w * ratio), height)
        elif height == 0:
            ratio = width / float(w)
            dim = (width, int(h * ratio))

        resized = cv.resize(img, dim, interpolation=inter)

        return resized
