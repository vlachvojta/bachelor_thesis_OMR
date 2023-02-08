#!/usr/bin/python3.8

import argparse
import re
import sys
import os
from common import Common
import time
import numpy as np
import matplotlib.pyplot as plt
import jiwer


class Evaulate_predictions:
    def __init__(self, ground_truth: str, input_files: list = [],
                 output_file: str = 'evaulated.txt') -> None:

        ground_truth = Common.read_file(ground_truth)
        ground_truth = [line for line in re.split(r'\n', ground_truth)
                        if not line == '']

        input_files = [file for file in input_files if os.path.isfile(file)]

        wers = [100]
        iterations = [0]

        for file_name in input_files[1:]:
            file = Common.read_file(file_name)
            file = [line for line in re.split(r'\n', file) if not line == '']
            wer = jiwer.wer(ground_truth, file) * 100
            iteration = int(re.findall(r'checkpoint_\d+', file_name)[0][11:])
            iterations.append(iteration)
            print(f'Iteration: {iteration} wer: {wer:.2f}%')
            wers.append(wer)

        print(iterations)
        print(wers)
        print(type(wers), type(iterations))

        plt.title('SSemantic symbol error')
        plt.plot(np.array(iterations), np.array(wers))
        plt.xlabel('Iteration')
        plt.ylabel('Symbol error [%]')

        plt.savefig('SAgnostic Symnbol Error.png')


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input_files", nargs='+',
        help=("Input prediction files to evaluate."))
    parser.add_argument(
        "-o", "--output_file", default='evaulated.txt',
        help=("Output folder to write evaluations to."))
    parser.add_argument(
        "-g", "--ground_truth", required=True,
        help=("Ground truth to compare files with."))
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    Evaulate_predictions(
        input_files=args.input_files,
        output_file=args.output_file,
        ground_truth=args.ground_truth)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
