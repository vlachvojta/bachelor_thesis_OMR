#!/usr/bin/python3.8
"""Simple script to evaluate checkpoint outputs created while training newer version of PERO
Example run:
$ python3 evaluate_checkpoints.py --ground-truth data.tst \
        --checkpoint-folder checkpoints
"""

import argparse
import re
import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
# import jiwer
from customwer import CustomWer

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class EvaulateCheckpoints:
    """Evaluate checkpoints is simple class to evaluate folder
    of training outputs and export to json and chart.
    """

    ERROR_ERROR = 100.42

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

        results = {}
        for file_name in input_files:
            iteration = int(re.findall(r"\d+", file_name)[-1])

            wer, cer = self.get_errs(file_name, ground_truth)

            results[iteration] = {'iter': iteration, 'wer': wer, 'cer': cer}
            print(f'Iteration: {iteration} wer: {results[iteration]}')

        self.make_chart(results, output_folder, name)

        json_file_path = os.path.join(output_folder, name + '.json')
        Common.write_to_file(results, json_file_path)

        print(f'Chart and json file saved to {output_folder}')

    def get_errs(self, file_name, ground_truth):
        """Get WER and CER of file."""
        file = Common.read_file(file_name)
        file = [line for line in re.split(r'\n', file) if not line == '']

        if len(ground_truth) != len(file):
            return self.ERROR_ERROR, self.ERROR_ERROR

        # Custom wer with continues counting
        my_wer = CustomWer()

        # Add lines in two different ways to demonstrate
        for gt, pred in zip(ground_truth[:50], file[:50]):
            my_wer.add_lines(gt, pred)
        my_wer.add_lines(ground_truth[50:], file[50:])

        cer = self.get_cerr(ground_truth, file)
        return my_wer(), cer

    def get_cerr(self, truth, result) -> float:
        # TODO Count Levenshtein distance same as in PERO
        return self.ERROR_ERROR

    def make_chart(self, results, output_folder, name):
        """Generate chart with iterations, WERs and CERs"""
        iterations = [results[res]['iter'] for res in results]
        wers = [results[res]['wer'] for res in results]
        cers = [results[res]['cer'] for res in results]

        # TODO add CER to chart
        plt.title(name)
        plt.plot(np.array(iterations), np.array(wers), label = 'Symbol error rate')
        plt.plot(np.array(iterations), np.array(cers), label = 'Character error rate')
        plt.xlabel('Iteration')
        plt.ylabel('Rate [%]')
        plt.legend()

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        plt.savefig(os.path.join(output_folder, name + '.png'))


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
        "-o", "--output-folder", type=str, default='evaluated_checkpoints',
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
