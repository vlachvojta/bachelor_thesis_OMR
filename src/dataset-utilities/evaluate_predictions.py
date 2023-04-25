#!/usr/bin/python3.8
"""Simple script to evaluate predictions from trained models

Example run:
$ python3.8 evaluate_predictions.py -ground-truth data.tst \
        --input-files checkpoint*.pth.out

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import argparse
import re
import os
from common import Common
import time
import numpy as np
import matplotlib.pyplot as plt
import jiwer


class Evaulate_predictions:
    def __init__(self, ground_truth: str, input_files: list = [],
                 output_file: str = 'evaulated.txt',
                 name: str = 'Evaluated_checkpoints') -> None:

        ground_truth = Common.read_file(ground_truth)
        ground_truth = [line for line in re.split(r'\n', ground_truth)
                        if not line == '']

        input_files = [file for file in input_files if os.path.isfile(file)]

        wers = []
        iterations = []

        for file_name in input_files:
            file = Common.read_file(file_name)
            file = [line for line in re.split(r'\n', file) if not line == '']

            if len(ground_truth) != len(file):
                continue

            # TODO kontroluj ID řádků pro každý řádek
            gt_first_ID = re.split(r'\s+', ground_truth[0])[0]
            pred_first_ID = re.split(r'\s+', file[0])[0]
            if not gt_first_ID == pred_first_ID:
                print('NOT MATCHING line IDs, Aborting')
                exit()

            wer = jiwer.wer(ground_truth, file) * 100
            # print(f'\t{jiwer.wer(ground_truth[0], file[0])},\n\tgt: {ground_truth[0]},\n\tpred: {file[0]}')
            cerr = self.get_cerr_mean(ground_truth, file)

            iteration = int(re.findall(r"\d+", file_name)[-1])
            iterations.append(iteration)
            print(f'Iteration: {iteration} wer: {wer:.2f}%')
            wers.append(wer)

        print(f'Iterations: {iterations}')
        print(f'WERs: {wers}')

        plt.title(name)
        plt.plot(np.array(iterations), np.array(wers))
        plt.xlabel('Iteration')
        plt.ylabel('Symbol error rate [%]')

        plt.savefig(name + '.png')
        # TODO save also text log to output_folder

    def get_cerr_mean(self, truth, result) -> float:
        # TODO Count Levenshtein distance
        return 0


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-files", nargs='+',
        help=("Input prediction files to evaluate."))
    # TODO implement output_folder instead of output_file
    parser.add_argument(
        "-o", "--output-file", default='evaulated.txt',
        help=("Output folder to write evaluations to."))
    parser.add_argument(
        "-g", "--ground-truth", required=True,
        help=("Ground truth to compare files with."))
    parser.add_argument(
        "-n", "--name", nargs='?', type=str, default='Evaluated_checkpoints',
        help=("Name of generated chart file + chart heading."))
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    Evaulate_predictions(
        input_files=args.input_files,
        output_file=args.output_file,
        ground_truth=args.ground_truth,
        name=args.name)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
