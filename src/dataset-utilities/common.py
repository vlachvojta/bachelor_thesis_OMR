#!/usr/bin/python3.8


import pathlib
import os
import sys


class Common:
    """Class for common tasks with dataset."""

    @staticmethod
    def print_dict(data: dict):
        print('{')
        keys = sorted(list(data.keys()))
        print(keys)
        for key in keys:
            print(f'\t{key}: {data[key]}')
        print('}')

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
