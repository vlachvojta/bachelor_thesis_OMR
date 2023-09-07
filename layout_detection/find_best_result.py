#!/usr/bin/python3.8
"""Finds best checkpoint of music_staff_detection training
    using results.csv in individual folders of training experiments.
"""

import argparse
import sys
import os
import time
import csv
import re


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", default='.',
        help="Path where to look for folders with results.csv files.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    BestResultFinder(
        path=args.path)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


class BestResultFinder:
    best_results = {}
    best_results_with_checkpoint = {}

    """Get label-image pairs from two separate folders."""
    def __init__(self, path: str = ''):
        if not path:
            path = os.getcwd()

        if path and not os.path.exists(path):
            raise FileNotFoundError(f'Path ({path}) not found')

        folders = []
        for f in os.listdir(path):
            folder_with_path = os.path.join(path, f)
            if os.path.isdir(folder_with_path) and os.path.isfile(os.path.join(folder_with_path, 'results.csv')):
                folders.append(f)

        print(f'Found {len(folders)} folders with results.csv files: {folders}')

        for folder in folders:
            self.find_best_result(path, folder, 'results.csv')

        all_folders = set(list(self.best_results.keys()) + list(self.best_results_with_checkpoint.keys()))
        print(f'All folders: {all_folders}')

        print()
        print('Best results in folders:')
        for folder in sorted(all_folders):
            print(f'{folder}')
            if folder in self.best_results_with_checkpoint:
                print(f'\t {self.best_results_with_checkpoint[folder]["result"]} '
                      f'in epoch {self.best_results[folder]["epoch"]}')
            if folder in self.best_results:
                print(f'\t({self.best_results[folder]["result"]} in epoch {self.best_results[folder]["epoch"]})')

        BestResultFinder.print_best_result(self.best_results)
        BestResultFinder.print_best_result(self.best_results_with_checkpoint, with_checkpoint=True)

    def find_best_result(self, path, folder, results_name: str):
        results_file = os.path.join(path, folder, 'results.csv')
        if not os.path.isfile(results_file):
            raise FileNotFoundError(f'Result file ({results_file}) not found')

        with open(results_file, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            _ = next(csv_reader)

            results = {}
            for row in csv_reader:
                epoch = row[0].strip()
                metric = row[7].strip()
                results[int(epoch)] = float(metric)

        best_epoch = max(results, key=results.get)
        self.best_results[folder] = {'epoch': best_epoch, 'result': results[best_epoch]}

        checkpoints = os.listdir(os.path.join(path, folder, 'weights'))
        pattern = r'[a-zA-Z]*(\d+)\.pt\S*'
        checkpoints = [re.match(pattern, c).group(1) for c in checkpoints if re.match(pattern, c)]
        checkpoints = [int(checkpoint) for checkpoint in checkpoints]
        # print(checkpoints)

        results_with_checkpoints = {}
        for checkpoint in checkpoints:
            results_with_checkpoints[checkpoint] = results[checkpoint]

        # print()
        # print(results_with_checkpoints)

        best_epoch = max(results_with_checkpoints, key=results_with_checkpoints.get)
        self.best_results_with_checkpoint[folder] = {'epoch': best_epoch, 'result': results[best_epoch]}

    @staticmethod
    def print_best_result(result_dict, with_checkpoint: bool = False):
        best_result = max(result_dict, key=lambda x: result_dict[x]['result'])

        print()
        if with_checkpoint:
            print(f'Best result WITH checkpoint:')  # {result_dict} ')
        else:
            print(f'Best result:')  # {result_dict} ')
        epoch = result_dict[best_result]["epoch"]
        print(f'\t{result_dict[best_result]["result"]} in {best_result}/{epoch}')
        print(f'\t=>{best_result}/weights/epoch{epoch}.pt')
        print()


if __name__ == "__main__":
    main()
