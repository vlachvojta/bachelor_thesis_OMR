#!/usr/bin/python3.8

import argparse
import re
import sys
import os
from common import Common
import time
import numpy as np
import matplotlib.pyplot as plt


class Log_visualizer:
    def __init__(sefl, file: str = "stdin", output: str = "log_out",
                 name: str = "") -> None:
        if file == "stdin":
            print('Input form stdin not supported yet, use file instead')
            exit()

        if not os.path.exists(output):
            os.mkdir(output)

        log = Common.read_file(file)
        cerrs = Log_visualizer.get_cerrs(log)
        print(f'cerrs[0:10]: {list(cerrs.values())[0:10]}')

        Log_visualizer.chart(cerrs, output, name)

        Log_visualizer.write_cerrs(cerrs, output, name)

        # print mean
        mean = np.mean(list(cerrs.values())[10:])
        print(f'mean of cerrs[10:] is: {mean}')

    @staticmethod
    def write_cerrs(cerrs: dict = {}, output: str = '',
                    name: str = 'fig_01') -> None:
        name = os.path.join(output, f'{name}.json')
        Common.write_to_file(cerrs, name)
        print(f'json written to: {name}')

    @staticmethod
    def get_cerrs(input: str = '') -> dict:
        input = input.split('ITERATION ')
        cerrs = {}

        for line in input:
            iteration = re.findall(r'\d+', line)
            if not iteration:
                continue
            iteration = int(iteration[0])

            cer = re.findall(r'cer\:\d+\.\d+', line)
            if not cer:
                continue

            cer = float(cer[-1][4:])
            cerrs[iteration] = cer
        return cerrs

    @staticmethod
    def chart(data: dict = {}, output: str = "", name: str = "fig_01") -> None:
        iterations = np.array(sorted(data.keys()))
        cerrs = np.array([data[k] for k in sorted(data.keys())])

        plt.title(name)
        plt.plot(iterations, cerrs)
        plt.xlabel('Iteration')
        plt.ylabel('Character error [%]')

        plt.savefig(os.path.join(output, f'{name}.png'))


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input_file", nargs='?', default='stdin',
        help=("Input log file to visualize."))
    parser.add_argument(
        "-o", "--output_folder", nargs='?', default='log_out',
        help=("Output folder."))
    parser.add_argument(
        "-n", "--name", nargs='?',
        help=("Name of generated chart file + chart heading."))
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    Log_visualizer(
        file=args.input_file,
        output=args.output_folder,
        name=args.name)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()