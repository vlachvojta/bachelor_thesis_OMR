#!/usr/bin/python3.8


class Common:
    """Class for common tasks with dataset."""

    def print_dict(data: dict):
        print('{')
        keys = sorted(list(data.keys()))
        print(keys)
        for key in keys:
            print(f'\t{key}: {data[key]}')
        print('}')
