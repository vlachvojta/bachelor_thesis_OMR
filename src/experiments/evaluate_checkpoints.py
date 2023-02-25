#!/usr/bin/python3.8
"""Simple script to evaluate checkpoint outputs created while training newer version of PERO
Example run:
$ python3.8 evaluate_checkpoints.py --ground-truth data.tst \
        --checkpoint-folder checkpoints
"""

import argparse
import re
import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import jiwer
from customwer import CustomWer


rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class EvaulateCheckpoints:
    """Evaluate checkpoints is simple class to evaluate folder
    of training outputs and export to json and chart.
    """
    def __init__(self, input_files: list, ground_truth: str,
                 output_folder: str = 'eval_out',
                 name: str = 'Evaluated_checkpoints') -> None:

        print(f'input_files: {input_files}')

        # Read Ground_truth
        ground_truth = Common.read_file(ground_truth)
        ground_truth = [line for line in re.split(r'\n', ground_truth)
                        if not line == '']

        # Check input files
        input_files = [file for file in input_files if os.path.isfile(file)]

        wers = []
        iterations = []

        for file_name in input_files:
            file = Common.read_file(file_name)
            file = [line for line in re.split(r'\n', file) if not line == '']

            if len(ground_truth) != len(file):
                continue

            wer_list = []
            for gt, pred in zip(ground_truth, file):
                wer_list.append(jiwer.wer(gt, pred) * 100)

            # Custom wer with continues counting
            wer_list = []
            my_wer = CustomWer()
            
            # Add lines in to different ways to demonstrate
            for gt, pred in zip(ground_truth[:50], file[:50]):
                my_wer.add_lines(gt, pred)
            my_wer.add_lines(ground_truth[50:], file[50:])

            wer_list.append(my_wer())

            cerr = self.get_cerr_mean(ground_truth, file)

            iteration = int(re.findall(r"\d+", file_name)[-1])
            iterations.append(iteration)
            print(f'Iteration: {iteration} wer: {my_wer():.2f}%')
            wers.append(my_wer())

        print(f'Iterations: \t{iterations}')
        print(f'WERs: \t\t{wers}')

        plt.title(name)
        plt.plot(np.array(iterations), np.array(wers))
        plt.xlabel('Iteration')
        plt.ylabel('Symbol error rate [%]')

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        plt.savefig(os.path.join(output_folder, name + '.png'))
        # TODO save also JSON log to output_folder

        print(f'Stuff saved to {output_folder}')

    def get_cerr_mean(self, truth, result) -> float:
        # TODO Count Levenshtein distance
        return 0


def parseargs():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-files", nargs='+',
        help="Folder where to look for checkpoint outputs.")
    parser.add_argument(
        "-g", "--ground-truth", required=True,
        help="Ground truth to compare files with.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='eval_out',
        help="Output folder to write outputs to.")
    parser.add_argument(
        "-n", "--name", type=str, default='Evaluated_checkpoints',
        help="Name of generated files + chart heading.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    EvaulateCheckpoints(
        input_files=args.input_files,
        ground_truth=args.ground_truth,
        output_folder=args.output_folder,
        name=args.name)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
