#!/usr/bin/python3.8
"""Finds best checkpoint of music_staff_detection training
    using results.csv in individual folders of training experiments.
"""

import argparse
import sys
import os
import time
import csv


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

        print(self.best_results)

        best_result = max(self.best_results, key=lambda x: self.best_results[x]['result'])
        print()
        print(f'Best result: {best_result} ')
        print(f'\tin epoch {self.best_results[best_result]["epoch"]}')
        print(f'\twith metric {self.best_results[best_result]["result"]}')
        print()

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


if __name__ == "__main__":
    main()
