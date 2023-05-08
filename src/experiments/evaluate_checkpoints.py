#!/usr/bin/python3.8
"""Simple script to evaluate checkpoint outputs created while training newer version of PERO

Usage:
$ python3 evaluate_checkpoints.py \
    --input-files checkpoints/checkpoint_*.pth.tst_out \
    --ground-truths checkpoints/ground_truth*.tst_out

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import argparse
import re
import sys
import os
import time
import logging
import numpy as np
import matplotlib.pyplot as plt
from customwer import CustomWer

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402
from pitch_rhythm_separator import PRSeparator #, Language


class EvaulateCheckpoints:
    """Evaluate checkpoints is simple class to evaluate folder
    of training outputs and export to json and chart.
    """

    ERROR_ERROR = 200.42
    EMPTY_PITCH = '@'

    def __init__(self, input_files: list, ground_truths: list,
                 output_folder: str = 'evaluated_checkpoints',
                 name: str = 'Evaluated_checkpoints',
                 ignore_n_pred: int = 0,
                 ignore_n_gt: int = 0,
                 verbose: bool = False) -> None:
        self.output_folder = output_folder
        self.verbose = verbose
        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO,format='[%(levelname)-s]\t- %(message)s')

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

        self.language = self.get_language(self.ground_truths)

        # Check input files
        input_files = [file for file in input_files if os.path.isfile(file)]

        if not input_files:
            print('INFO: No files loaded, ending.')
            return

        print(f'Getting data from {len(input_files)} files.')

        self.results = Results()
        for file_name in input_files:
            file_name_base = os.path.basename(file_name)
            if re.match(r'checkpoint_\d+(\.pth)\.tst_out', file_name_base):
                set_id = ''
            else:
                splitted = re.split(r'checkpoint_\d+|(\.pth)?\.tst_out', file_name_base)

                if len(splitted) == 3:
                    set_id = splitted[1] if splitted[1] else ''
                elif len(splitted) == 5:
                    set_id = splitted[2] if splitted[2] else ''
                else:
                    print(f'INFO: No test set id found in file_name ({file_name}), SKIPPING.')
                    continue

            if set_id not in self.ground_truths:
                print(f'INFO: No ground_truth for set id ({set_id}), SKIPPING.')
                continue

            iteration = int(re.findall(r"\d+", file_name)[0])

            cer, wer, pitch_ser, rhythm_ser, seq_err  = self.get_errs(
                file_name, self.ground_truths[set_id], ignore_n_pred)

            if wer == cer == pitch_ser == rhythm_ser == seq_err == self.ERROR_ERROR:
                continue

            self.results.add_result(iteration, set_id, wer, cer, pitch_ser, rhythm_ser, seq_err)

            self.results.print_results_of_iteration_with_set_id(iteration, set_id)

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # Print charts
        for set_id in self.results.get_set_ids():
            if self.results.len >= 20:
                self.make_chart(f'{name}{set_id}', threshold=self.results.len // 2,
                                print_pitch_and_rhythm = True, set_select=set_id)
            self.make_chart(f'{name}{set_id}', threshold=0,
                            print_pitch_and_rhythm = True, set_select=set_id)

        if self.results.len >= 20:
            self.make_chart(f'{name}_all', threshold=self.results.len // 2)

        self.make_chart(f'{name}_all', threshold=0)

        # Save results to json file
        json_file_path = os.path.join(output_folder, name + '.json')
        self.results.save_to_file(json_file_path)
        print(f'Chart(s) and json file saved to {output_folder}')

        for set_id in self.results.get_set_ids():
            self.results.print_minimal_wer_of_set(set_id)

    def get_language(self, ground_truths: dict) -> int:
        """Get language from ground truths using PRSeparator funcion."""
        languages = []

        for set_id, gts in ground_truths.items():
            languages.append(PRSeparator.guess_label_language(gts[0]))
            print(languages[-1])

        return languages[0]

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

    def get_errs(self, file_name, ground_truth, ignore_n_words: int = 0
                ) -> (float, float, float, float, float):
        """Get CER, WER, pitch_SER, rhythm_SER and Sequence error of file."""
        file = Common.read_file(file_name)
        file = [line for line in re.split(r'\n', file) if not line == '']
        if ignore_n_words > 0:
            file = self.ignore_n_words(ignore_n_words, file)

        if len(ground_truth) != len(file):
            if len(file) % len(ground_truth) == 0:
                times = len(file) // len(ground_truth)
                print(f'INFO: file is {times} times longer than ground truth.'
                      ' Using only last part of matching length.')
                file = file[-len(ground_truth):]
            else:
                print(f'WARNING: Number of lines in ground truth ({len(ground_truth)}) '
                    f'and file ({len(file)}) do not match. SKIPPING.')
                return self.ERROR_ERROR, self.ERROR_ERROR, self.ERROR_ERROR, self.ERROR_ERROR, self.ERROR_ERROR

        # Custom wer with continues counting
        my_wer = CustomWer()
        pitch_err = CustomWer()
        rhythm_err = CustomWer()

        # Add lines in two different ways to demonstrate
        for truth, pred in zip(ground_truth[:50], file[:50]):
            my_wer.add_lines(truth, pred)
        my_wer.add_lines(ground_truth[50:], file[50:])

        for truth, pred in zip(ground_truth, file):
            pred_pitch, pred_rhythm = PRSeparator.separate_labels(pred, self.language)
            truth_pitch, truth_rhythm = PRSeparator.separate_labels(truth, self.language)

            if not truth_pitch or re.match(r'^\s+$', truth_pitch):
                truth_pitch = self.EMPTY_PITCH
            if not pred_pitch or re.match(r'^\s+$', pred_pitch):
                pred_pitch = self.EMPTY_PITCH

            # print(f'final language is: {self.language}')
            # print(f'truth: {truth}')
            # print(f'    pser: ({truth_pitch})')
            # print(f'    rser: {truth_rhythm}')

            # print(f'pred: {pred}')
            # print(f'    pser: ({pred_pitch})')
            # print(f'    rser: {pred_rhythm}')

            pitch_err.add_lines(truth_pitch, pred_pitch)
            rhythm_err.add_lines(truth_rhythm, pred_rhythm)

        return my_wer(get='cer'), my_wer(), pitch_err(), rhythm_err(), my_wer(get='seqer')

    def make_chart(self, name, threshold: int = 0, print_pitch_and_rhythm: bool = False,
                   set_select: str = None):
        """Generate chart with iterations, WERs and CERs

        If set_id is None, print all sets to one chart."""
        colors_default = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#17bcef']

        if set_select is None:
            sets = self.results.get_set_ids()
            color_sets = [[color] * 5 for color in colors_default]
        elif set_select in self.results.get_set_ids():
            sets = [set_select]
            color_sets = [colors_default]
        else:
            print(f'Set {set_select} not found, not printing.')
            return

        for set_id, color_set in zip(sets, color_sets):
            wer_iterations, wers = self.results.get_wers(set_id, threshold)
            cer_iterations, cers = self.results.get_cers(set_id, threshold)

            if print_pitch_and_rhythm:
                p_ser_iterations, p_sers = self.results.get_pitch_ser(set_id, threshold)
                r_ser_iterations, r_sers = self.results.get_rhythm_ser(set_id, threshold)
                seqer_iterations, seqers = self.results.get_seqer(set_id, threshold)

            wer_label = 'Symbol Error Eate'
            cer_label = 'Character Error Eate'
            pitch_label = 'Pitch Error Eate'
            rhythm_label = 'Rhythm Error Rate'
            seqer_label = 'Sequence Error Rate'

            if set_select is None and len(sets) > 1:
                wer_label += f' for set {set_id}'
                cer_label += f' for set {set_id}'
                pitch_label += f' for set {set_id}'
                rhythm_label += f' for set {set_id}'
                seqer_label += f' for set {set_id}'

            # fig, ax = plt.subplots()
            plt.title(name)
            plt.plot(wer_iterations, np.array(wers), color=color_set[0], label = wer_label)
            plt.plot(cer_iterations, np.array(cers), ':', color=color_set[1], label = cer_label)
            if print_pitch_and_rhythm:
                plt.plot(p_ser_iterations, np.array(p_sers), "-.",
                         color=color_set[2], label = pitch_label)
                plt.plot(r_ser_iterations, np.array(r_sers), '--' ,
                         color=color_set[3], label = rhythm_label)
                plt.plot(seqer_iterations, np.array(seqers),
                         color=color_set[4], label = seqer_label)

        plt.xlabel('Počet trénovacích epoch')
        plt.ylabel('Chybovost přepisů [%]')
        plt.legend()

        if threshold > 0:
            chart_out_png = os.path.join(self.output_folder, f'{name}_part.png')
            chart_out_svg = os.path.join(self.output_folder, f'{name}_part.svg')
        else:
            chart_out_png = os.path.join(self.output_folder, f'{name}.png')
            chart_out_svg = os.path.join(self.output_folder, f'{name}.svg')
        plt.savefig(chart_out_png)
        plt.savefig(chart_out_svg)
        print(f'Chart saved to {chart_out_png}')
        print(f'           and {chart_out_svg}')
        plt.clf()
        # TODO export vector graphs

class Results:
    """Simple class to store error results and return in correct format to make charts."""
    results: dict
    set_ids: set

    EMPTY = 200.42

    def __init__(self):
        self.results = {}
        self.set_ids = set()

    def add_result(self, iteration, set_id, wer, cer, pitch_ser, rhythm_ser, seq_err) -> None:
        dict_to_add = {'wer': wer, 'cer': cer, 'pitch_ser': pitch_ser, 'rhythm_ser': rhythm_ser, 'seqer': seq_err}

        if iteration in self.results:
            self.results[iteration][set_id] = dict_to_add
        else:
            self.results[iteration] = {set_id: dict_to_add}

        self.set_ids.add(set_id)

    def get_data(self) -> dict:
        return self.results

    def get_iterations(self) -> list:
        return sorted(self.results.keys())

    def get_results_of(self, set_id, threshold, key = 'wer'):
        values = []
        iterations = []

        for iteration in self.get_iterations()[threshold:]:
            if set_id in self.results[iteration]:
                values.append(self.results[iteration][set_id][key])
                iterations.append(iteration)

        return iterations, values

    def get_wers(self, set_id, threshold) -> (list, list):
        return self.get_results_of(set_id, threshold, 'wer')

    def get_cers(self, set_id, threshold) -> (list, list):
        return self.get_results_of(set_id, threshold, 'cer')

    def get_pitch_ser(self, set_id, threshold) -> (list, list):
        return self.get_results_of(set_id, threshold, 'pitch_ser')

    def get_rhythm_ser(self, set_id, threshold) -> (list, list):
        return self.get_results_of(set_id, threshold, 'rhythm_ser')

    def get_seqer(self, set_id, threshold) -> (list, list):
        return self.get_results_of(set_id, threshold, 'seqer')

    def get_set_ids(self):
        return sorted(self.set_ids)

    def __repr__(self) -> str:
        return str(self.results)

    def save_to_file(self, file_path: str) -> None:
        Common.write_to_file(self.results, file_path)

    def get_results_of_iteration(self, iteration, set_id) -> (float, float, float, float, float): #, set = None):
        """Get results of iteration. IF set is None, return results for all sets.
        
        Return cer, wer, pitch_ser, rhythm_ser, seq_err IN THIS ORDER
        """
        if not iteration in self.results or not set_id in self.results[iteration]:
            return [self.EMPTY] * 5

        result = self.results[iteration][set_id]

        return result['cer'], result['wer'], result['pitch_ser'], result['rhythm_ser'], result['seqer']

    def print_results_of_iteration(self, iteration) -> None:
        """Print Iteration from results."""
        for set_id in self.get_set_ids():
            self.print_results_of_iteration_with_set_id(iteration, set_id)

    def print_results_of_iteration_with_set_id(self, iteration, set_id) -> None:
        """Print Iteration from results."""
        ES = '' if set_id == '_0' else ' '    # ES = Extra Space

        cer, wer, pser, rser, seqer = self.get_results_of_iteration(iteration, set_id)
        print(f'It: {iteration} (set {set_id}), \t{ES}cer: {cer:.2f}, \t{ES}wer: {wer:.2f}, '
                f'\t{ES}seq_err: {seqer:.2f}'
                f'\t{ES}pitch_ser: {pser:.2f}, \t{ES}rhythm_ser: {rser:.2f}, ')

    def print_minimal_wer_of_set(self, set_id) -> None:
        iters, wers = self.get_wers(set_id, 0)
        tuples = list(zip(iters, wers))
        tuples = sorted(tuples, key=lambda x: x[1], reverse=True)

        print(f'Minimal WER found for set {set_id}:')
        self.print_results_of_iteration_with_set_id(tuples[-1][0], set_id)

    @property
    def len(self) -> int:
        return len(self.results)


def parseargs():
    """Parse arguments."""
    print(' '.join(sys.argv))
    Common.print_line_after_sys_argv()

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
    # parser.add_argument(
    #     "-l", "--label-language", type=str, default=None,
    #     help="Label language for translating back to the original.")
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
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
        ignore_n_pred=args.ignore_n_words_pred,
        verbose=args.verbose)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
