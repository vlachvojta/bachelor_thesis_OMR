#!/usr/bin/python3
"""Simple script to find the last checkpoint in folder.

Used for automatic continuing of paused experiments.
Usage: $python3 find_last_checkpoint.py experiment/checkpoints
"""


import re
import os
import argparse


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest='directory', help=("Folder where to look for checkpoints"))
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    if not os.path.exists(args.directory):
        print('0')
        return

    # print(f'found {len(os.listdir(args.directory))} files in directory')

    files = [file for file in os.listdir(args.directory)
            if re.fullmatch(r"checkpoint_\d+\.pth", file)]
    
    file_nums = []
    for file in files:
        file_name = re.split(r'\.', file)[0]
        file_number = file_name[11:]
        file_nums.append(file_number)
    
    number = max(file_nums)

    # number = re.split(r'\.', file)[0]
    # number = re.split(r'\_', number)[1]

    try:
        print(int(number))
    except ValueError:
        print('0')
    return


if __name__ == "__main__":
    main()
