#!/usr/bin/python3.8

import argparse
import re
import sys
from common import Common
import time


class Symbol_converter:
    """Module for converting symbols.

    Used to convert symbols from agnostic and semantic encoding
    to a shorter form and back.
    """

    dictionary = {}

    def __init__(self, dictionary_file: str = 'translator.agnostic.json',
                 input_files: list = [], output: str = 'stdout',
                 reverse: bool = False):
        print('\tSC: Hello form SYMBOL_CONVERTER (SC)')
        print(f'\tSC: dictionary: {dictionary_file}, input_files {input_files}'
              f', output: {output}, reverse: {reverse}')

        self.dictionary = Common.read_file(dictionary_file)

        if len(input_files) > 0:
            input_files = Common.check_existing_files(input_files)

            print(f'\tSC: Loading symbols from {len(input_files)} file(s).')
            symbols_in = self.load_symbols_from_files(input_files)
            print(f'\tSC: {len(symbols_in)} symbols loaded.')

            symbols_out = self.convert_list(symbols_in, reverse)

            if output == 'stdout':
                print(' '.join(symbols_out))
            else:
                Common.write_to_file(' '.join(symbols_out), output)

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

    def convert_list(self, symbols_in: list = [],
                     reverse: bool = False) -> list:
        symbols_out = []
        for sym in symbols_in:
            symbols_out.append(self.convert(sym, reverse=reverse))
        return symbols_out

    def convert(self, symbol: str = '', reverse: bool = False) -> str:
        """Convert symbol and back.

        if Direction is True, convert to smaller
        else convert to larger.
        """
        if reverse:
            dictionary = Symbol_converter._reverse_dict(self.dictionary)
        else:
            dictionary = self.dictionary

        try:
            return dictionary[symbol]
        except KeyError:
            print(f'\tSC: [INFO] Neexistující konverze pro symbol ({symbol})',
                  file=sys.stderr)
            return ''

    @staticmethod
    def _reverse_dict(data: dict = {}) -> dict:
        return {v: k for k, v in data.items()}


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
