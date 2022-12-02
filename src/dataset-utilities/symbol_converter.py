#!/usr/bin/python3.8

import argparse
import re
import sys
import os
from common import Common
import time


class Symbol_converter:
    """Module for converting symbols.

    Used to convert symbols from agnostic and semantic encoding
    to a shorter form and back.
    """

    def __init__(self, input_files: list = [], output: str = [],
                 reverse: bool = False):
        print('Hello form SYMBOL_CONVERTER')
        print(f'input_files {input_files}, output: {output}, '
              f'reverse: {reverse}')

        input_files = Common.check_existing_files(input_files)

        print(f'Loading symbols from {len(input_files)} file(s).')
        symbols_in = self.load_symbols_from_files(input_files)
        print(f'{len(symbols_in)} symbols loaded.')

        output_symbols = Symbol_converter.convert_symbols(symbols_in)

        Common.write_to_file(' '.join(output_symbols), output)

    def load_symbols_from_files(self, files: list = []) -> list:
        symbols_in = []
        for file in files:
            new_symbols = Common.read_file(file)

            if isinstance(new_symbols, dict):
                for v in new_symbols.values():
                    symbols_in += v
            elif isinstance(new_symbols, list):
                symbols_in += new_symbols
            elif isinstance(new_symbols, str):
                new_symbols = re.split(r'\s', new_symbols)
                symbols_in += [s for s in new_symbols if s]
            else:
                raise ValueError('Loaded file has unknown format of data.')
        return symbols_in

    @staticmethod
    def convert_symbols(symbols_in: list = []) -> list:
        return symbols_in


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input_files", nargs='*', default=[],
        help=("Files to read symbols from, you can add more files.\n" +
              "USE FULL FILE PATH (relative or absolute)"))
    parser.add_argument(
        "-o", "--output_file", default='stdout',
        help="Set output file with extension. Output format is JSON")
    parser.add_argument(
        "-r", "--reverse", default=False, action='store_true',
        help="Reverse conversion. Convert shorter to larger tokens.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    Symbol_converter(
        input_files=args.input_files,
        output=args.output_file,
        reverse=args.reverse)

    end = time.time()
    print(f'Total time: {end - start}')


if __name__ == "__main__":
    main()
