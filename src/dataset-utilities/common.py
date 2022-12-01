#!/usr/bin/python3.8


import pathlib
import os
import sys
import json
import time

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
    def check_existing_files(files):
        """Return only existing file"""
        return [file for file in files if os.path.exists(file)]

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
            # TODO Continue implementing here.

        return existing_files

    @staticmethod
    def save_dict_as_json(data: dict, file: str) -> None:
        with open(file, 'w') as fp:
            json.dump(data, fp)

    @staticmethod
    def read_file(file: str):
        """Read file, method assumes, file exists."""
        if not os.path.exists(file):
            return

        file_extension = file.split('.')[-1]
        with open(file) as f:
            if file_extension == 'json':
                data = json.load(f)
            else:
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
        pjoin = os.path.join

        print(f'looking for all files in {folder}')
        # start = time.time()
        files = []
        dirs = []
        for f in Common.full_list(folder):
            if os.path.isdir(f):
                dirs.append(f)
            elif os.path.isfile(f) and Common.right_file_ext(f, exts):
                files.append(f)
        # end = time.time()
        # print(f'looking done, it took {end - start}')

        assert len(dirs) > 0

        if dirs:
            print(f'Looking for files in {len(dirs)} (every dot is 1000 dirs)')
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
