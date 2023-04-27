#!/usr/bin/python3.8
"""Simple script to evaluate checkpoint outputs created while training newer version of PERO
Example run:
$ python3 evaluate_checkpoints.py \
    --input-files checkpoints/checkpoint_*.pth.tst_out \
    --ground-truths checkpoints/ground_truth*.tst_out \
"""

import argparse
import re
import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from customwer import CustomWer

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class EvaulateCheckpoints:
    """Evaluate checkpoints is simple class to evaluate folder
    of training outputs and export to json and chart.
    """

    ERROR_ERROR = 200.42

    def __init__(self, input_files: list, ground_truths: list,
                 output_folder: str = 'evaluated_checkpoints',
                 name: str = 'Evaluated_checkpoints',
                 ignore_n_pred: int = 0,
                 ignore_n_gt: int = 0) -> None:
        # Read Ground_truth
        self.ground_truths = self.read_gound_truths(ground_truths, ignore_n_gt)
        del_keys = []
        for set_id, gt_labels in self.ground_truths.items():
            if len(gt_labels) == 0:
                print(f'WARNING: Ground-truth file for set {set_id} is empty, deleting key.')
                del_keys.append(set_id)

        for del_key in del_keys:
            del self.ground_truths[del_key]

        if self.ground_truths:
            print(f'INFO: Loaded {len(self.ground_truths)} groundtruths '
                  f'with sets: {list(self.ground_truths.keys())}')
        else:
            raise FileNotFoundError('No ground truth files found!')

        # Check input files
        input_files = [file for file in input_files if os.path.isfile(file)]

        self.results = Results()
        for file_name in input_files:
            file_name_base = os.path.basename(file_name)
            if re.match(r'checkpoint_\d+(\.pth)\.tst_out', file_name_base):
                set_id = ''
            else:
                splitted = re.split(r'checkpoint_\d+|(\.pth)?\.tst_out', file_name_base)

                if len(splitted) == 3:
                    set_id = splitted[1]
                elif len(splitted) == 5:
                    set_id = splitted[2]
                else:
                    print(f'INFO: No test set id found in file_name ({file_name}), SKIPPING.')
                    continue

            if set_id not in self.ground_truths:
                print(f'INFO: No ground_truth for set id ({set_id}), SKIPPING.')
                continue

            iteration = int(re.findall(r"\d+", file_name)[0])

            wer, cer = self.get_errs(file_name, self.ground_truths[set_id], ignore_n_pred)

            if wer == cer == self.ERROR_ERROR:
                continue

            self.results.add_result(iteration, set_id, wer, cer)

            print(f'Iteration: {iteration}, set_id: {set_id}, wer: {wer}, cer: {cer}')

        if self.results.len < 20:
            self.make_chart(self.results, output_folder, name, threshold=0)
        else:
            self.make_chart(self.results, output_folder, name, threshold=0)
            self.make_chart(self.results, output_folder, name, threshold=self.results.len // 2)

        self.make_chart(self.results, output_folder, name)

        json_file_path = os.path.join(output_folder, name + '.json')
        self.results.save_to_file(json_file_path)
        print(f'Chart(s) and json file saved to {output_folder}')

    def read_gound_truths(self, ground_truths: list, ignore_n_gt: int = 0) -> dict:
        """Read the ground truth files if exist.

        Returns a dictionary:
            k: name or id of the test set
            v: lines from the file
        """
        existing_files = [ground_truth for ground_truth in ground_truths
                          if os.path.isfile(ground_truth)]
        ground_truths_dict = {}

        for file in existing_files:
            # Get set_id
            gt_basename = os.path.basename(file)
            splitted = re.split(r'ground_truth|\.tst_out', gt_basename)

            if not len(splitted) == 3:
                raise NameError('Ground truth file name has wrong format. '
                                'Cannot separate test set names.')
            set_id = splitted[1]

            # Read file
            ground_truth = Common.read_file(file)
            ground_truth = [line for line in re.split(r'\n', ground_truth)
                            if not line == '']
            if ignore_n_gt > 0:
                ground_truth = self.ignore_n_words(ignore_n_gt, ground_truth)

            ground_truths_dict[set_id] = ground_truth

        return ground_truths_dict

    def ignore_n_words(self, ignore_n_words: int, file: list) -> None:
        """Ignore n words in a file."""
        new_file = []

        for line in file:
            splited = re.split(r'\s+', line)
            if len(splited) > ignore_n_words:
                new_line = ' '.join(splited[ignore_n_words:])
                new_file.append(new_line)

        return new_file

    def get_errs(self, file_name, ground_truth, ignore_n_words: int = 0) -> tuple:
        """Get WER and CER of file."""
        file = Common.read_file(file_name)
        file = [line for line in re.split(r'\n', file) if not line == '']
        if ignore_n_words > 0:
            file = self.ignore_n_words(ignore_n_words, file)

        if len(ground_truth) != len(file):
            if len(file) % len(ground_truth) == 0:
                times = len(file) // len(ground_truth)
                print(f'INFO: file is {times} times longer than ground truth.'
                      ' Using only last part of mathing length.')
                file = file[-len(ground_truth):]
            else:
                print(f'ERR: Number of lines in ground truth ({len(ground_truth)}) '
                    f'and file ({len(file)}) do not match. SKIPPING.')
                return self.ERROR_ERROR, self.ERROR_ERROR

        # Custom wer with continues counting
        my_wer = CustomWer()

        # Add lines in two different ways to demonstrate
        for truth, pred in zip(ground_truth[:50], file[:50]):
            my_wer.add_lines(truth, pred)
        my_wer.add_lines(ground_truth[50:], file[50:])

        return my_wer(), my_wer(get='cer')

    def make_chart(self, results, output_folder, name, threshold: int = 0):
        """Generate chart with iterations, WERs and CERs"""
        set_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']

        for set_id, set_color in zip(results.get_set_ids(), set_colors):
            # set_id = results.get_set_ids()[1]
            # set_color = set_colors[0]
            # iterations = results.get_iterations()
            wer_iterations, wers = results.get_wers(set_id, threshold)
            cer_iterations, cers = results.get_cers(set_id, threshold)

            if len(results.get_set_ids()) == 1:
                wer_label = 'Symbol error rate'
                cer_label = 'Character error rate'
            else:
                wer_label = f'Symbol error rate for set {set_id}'
                cer_label = f'Character error rate for set {set_id}'


            # fig, ax = plt.subplots()
            plt.title(name)
            plt.plot(wer_iterations, np.array(wers), color=set_color, label = wer_label)
            plt.plot(cer_iterations, np.array(cers), ':', color=set_color, label = cer_label)

        plt.xlabel('Iteration')
        plt.ylabel('Rate [%]')
        plt.legend()

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if threshold > 0:
            chart_out = os.path.join(output_folder, name + '_part.png')
            plt.savefig(chart_out)
        else:
            chart_out = os.path.join(output_folder, name + '.png')
            plt.savefig(chart_out)
        print(f'Chart saved to {chart_out}')
        plt.clf()
        # TODO export vector graphs

class Results:
    """Simple class to store error results and return in correct format to make charts."""
    results: dict
    set_ids: set

    def __init__(self):
        self.results = {}
        self.set_ids = set()

    def add_result(self, iteration, set_id, wer,cer) -> None:
        if iteration in self.results:
            self.results[iteration][set_id] = {'wer': wer, 'cer': cer}
        else:
            self.results[iteration] = {set_id: {'wer': wer, 'cer': cer}}

        self.set_ids.add(set_id)

    def get_data(self) -> dict:
        return self.results

    def get_iterations(self) -> list:
        return sorted(self.results.keys())

    def get_wers(self, set_id, threshold) -> (list, list):
        wers = []
        wer_iterations = []

        for iteration in self.get_iterations()[threshold:]:
            if set_id in self.results[iteration]:
                wers.append(self.results[iteration][set_id]['wer'])
                wer_iterations.append(iteration)

        return wer_iterations, wers

    def get_cers(self, set_id, threshold) -> (list, list):
        cers = []
        cer_iterations = []

        for iteration in self.get_iterations()[threshold:]:
            if set_id in self.results[iteration]:
                cers.append(self.results[iteration][set_id]['cer'])
                cer_iterations.append(iteration)

        return cer_iterations, cers

    def get_set_ids(self):
        return sorted(self.set_ids)

    def __repr__(self) -> str:
        return str(self.results)

    def save_to_file(self, file_path: str) -> None:
        Common.write_to_file(self.results, file_path)

    @property
    def len(self) -> int:
        return len(self.results)


def parseargs():
    """Parse arguments."""
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-files", nargs='+',
        help="List of input files (checkpoint outputs)")
    parser.add_argument(
        "-g", "--ground-truths", nargs='+', required=True,
        help=("Ground truths to compare files with, "
              "number of ground truths determines how many sets are there."))
    parser.add_argument(
        "-o", "--output-folder", type=str, default='evaluated_checkpoints',
        help="Output folder to write outputs to.")
    parser.add_argument(
        "-n", "--name", type=str, default='Evaluated_checkpoints',
        help="Name of generated files + chart heading.")
    parser.add_argument(
        "--ignore-n-words-gt", type=int, default=0,
        help="Ignore first n words in ground truth.")
    parser.add_argument(
        "--ignore-n-words-pred", type=int, default=0,
        help="Ignore first n words in checkpoint predictions.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    EvaulateCheckpoints(
        input_files=args.input_files,
        ground_truths=args.ground_truths,
        output_folder=args.output_folder,
        name=args.name,
        ignore_n_gt=args.ignore_n_words_gt,
        ignore_n_pred=args.ignore_n_words_pred)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
