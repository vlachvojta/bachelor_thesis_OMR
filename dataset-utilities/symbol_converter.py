#!/usr/bin/python3.8
"""Simple script for converting symbols using external translator dictionary.

Used to convert symbols from agnostic and semantic encoding to a shorter form and back.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import argparse
import re
import sys
import time

from common import Common


class SymbolConverter:
    """Module for converting symbols.

    Used to convert symbols from agnostic and semantic encoding
    to a shorter form and back.
    """

    dictionary = {}

    def __init__(self, translator_file: str = 'translator.agnostic.json',
                 input_files: list = [], output: str = 'stdout',
                 reverse: bool = False, mode: str = "orig"):
        print('\tHello form SYMBOL_CONVERTER (SC)')
        print(f'\tDictionary: {translator_file}, input_files {input_files}'
              f', output: {output}, reverse: {reverse}')

        self.dictionary = Common.read_file(translator_file)
        if not self.dictionary:
            print('ERR: No dictionary loaded, exiting', file=sys.stderr)
            sys.exit(1)
        self.mode = mode
        self.n_existing_labels = set()
        self.error_splitting_lines = set()

        if len(input_files) == 0:
            print('ERR: No input files, exiting', file=sys.stderr)
            sys.exit(1)

        input_files = Common.check_existing_files(input_files)

        print(f'\tLoading symbols from {len(input_files)} file(s).')
        input_ = self.load_symbols_from_files(input_files)

        if self.mode == 'orig':
            print(f'\t{len(input_)} symbols loaded.')
            symbols_out = self.convert_list(input_, reverse)

            if output == 'stdout':
                print(' '.join(symbols_out))
            else:
                Common.write_to_file(' '.join(symbols_out), output)
                print(f'Converted labels saved to {output}')
        elif self.mode == 'matchmaker':
            print(f'\tLoaded {len(input_)} lines of labels.')
            lines_out = self.convert_lines(input_, reverse)
            if output == 'stdout':
                print('\n'.join(lines_out))
            else:
                # print('\n'.join(lines_out[:20]))
                Common.write_to_file('\n'.join(lines_out), output)
                print(f'Converted labels saved to {output}')

        if len(self.n_existing_labels) > 0:
            print(f'Found {len(self.n_existing_labels)} not existing labels, please update translator')
            print(sorted(self.n_existing_labels))
        if len(self.error_splitting_lines) > 0:
            print(f'{len(self.n_existing_labels)} lines have different format than needed')
            print(sorted(self.n_existing_labels))


    def load_symbols_from_files(self, files: list = []) -> list:
        symbols_in = []
        for file in files:
            new_symbols = Common.read_file(file)
            if self.mode == 'matchmaker':
                symbols_in += re.split(r'\n', new_symbols)
            elif self.mode == 'orig':
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

    def convert_lines(self, lines_in, reverse: bool = False) -> list:
        """Convert lines from matchmaker labels database to converted symbols.
        
        Return list representing lines of converted symbols with stave ID."""
        output = []

        for line in lines_in:
            if not line:
                continue
            try:
                stave_id, labels, _ = re.split(r"\"+", line)
            except ValueError:
                self.error_splitting_lines.add(line)
                continue

            labels_orig = re.split(r"\s+", labels)
            labels_converted = self.convert_list(labels_orig, reverse)

            stave_id = self.get_correct_PERO_id(stave_id)

            output.append(f'{stave_id} "{" ".join(labels_converted)}"')

        return output

    def get_correct_PERO_id(self, stave_id: str) -> str:
        """Checks if stave_id is correct PERO_ID, must have png name + zero tag for LMDB."""
        if not stave_id:
            return ""

        img_id, *rest = re.split(r'\s', stave_id)

        if not img_id.endswith('.png'):
            img_id = f'{img_id}-{Common.PERO_LMDB_zero_tag}.png'
        else:
            img_id_withou_ext, *_ = re.split(r'\.', img_id)
            img_id = f'{img_id_withou_ext}-{Common.PERO_LMDB_zero_tag}.png'

        if len(rest) == 0:
            return f'{img_id} {Common.PERO_LMDB_zero_tag}'
        elif len(rest) == 1:
            return f'{img_id} {Common.PERO_LMDB_zero_tag}'
        elif len(rest) > 1:
            return f'{stave_id}'

    def convert_list(self, symbols_in: list = [],
                     reverse: bool = False) -> list:
        symbols_out = []
        for sym in symbols_in:
            if not sym:
                continue
            if sym.startswith('"'):
                sym = sym[1:]
            elif sym.endswith('"'):
                sym = sym[:-1]

            symbols_out.append(self.convert(sym, reverse=reverse))
        return symbols_out

    def convert(self, symbol: str = '', reverse: bool = False) -> str:
        """Convert symbol and back.

        If reverse, convert to smaller, else convert to larger.
        """
        if reverse:
            dictionary = SymbolConverter._reverse_dict(self.dictionary)
        else:
            dictionary = self.dictionary

        try:
            return dictionary[symbol]
        except KeyError:
            # print(f'\tSC: [INFO] Neexistující konverze pro symbol ({symbol})',
            #       file=sys.stderr)
            self.n_existing_labels.add(symbol)
            return ''

    @staticmethod
    def _reverse_dict(data: dict = {}) -> dict:
        if data:
            return {v: k for k, v in data.items()}
        return {}


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input_files", nargs='*', default=[],
        help=("Files to read symbols from, you can add more files.\n" +
              "USE FULL FILE PATH (relative or absolute)"))
    parser.add_argument(
        "-o", "--output_file", default='stdout',
        help="Set output file.")
    parser.add_argument(
        "-t", "--translator", default='translator.agnostic.json',
        help="JSON File containing translation dictionary.")
    parser.add_argument(
        "-m", "--mode", choices=['orig', 'matchmaker'], default='orig',
        help=("Mode of input data. Orig is first use, "
              "matchmaker is used to load labels from matchmaker output."))
    parser.add_argument(
        "-r", "--reverse", default=False, action='store_true',
        help="Reverse conversion. Convert shorter to larger tokens.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    SymbolConverter(
        input_files=args.input_files,
        output=args.output_file,
        reverse=args.reverse,
        translator_file=args.translator,
        mode=args.mode)

    end = time.time()
    print(f'Total time: {end - start}')


if __name__ == "__main__":
    main()
