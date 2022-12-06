#!/usr/bin/python3.8

import argparse
import re
import sys
import os
from common import Common
import time
from functools import partialmethod as partm
from functools import partial


class Symbol_converter:
    """Module for converting symbols.

    Used to convert symbols from agnostic and semantic encoding
    to a shorter form and back.
    """

    # Separators used in originla dataset
    SEPARATORS = r'-._'

    # Separator used in new converted dataset
    SEPARATOR = '_'

    def __init__(self, input_files: list = [], output: str = [],
                 reverse: bool = False):
        print('Hello form SYMBOL_CONVERTER')
        print(f'input_files {input_files}, output: {output}, '
              f'reverse: {reverse}')

        input_files = Common.check_existing_files(input_files)

        print(f'Loading symbols from {len(input_files)} file(s).')
        symbols_in = self.load_symbols_from_files(input_files)
        print(f'{len(symbols_in)} symbols loaded.')

        symbols_out = Symbol_converter.convert_list(symbols_in)

        Common.write_to_file(' '.join(symbols_out), output)

    @staticmethod
    def enlarge(symbol_in: str = '', actions: list = []):
        """Enlarge symbol back to original encoding

        Actions is list of instructions for individual chars of symbol.
        Options are:
            0 - leave it as is
            str - place string instead of original char
        """
        def resolve_int_or_str(action: any, char: str = '') -> str:
            if isinstance(action, int) and action == 0:
                return char
            elif isinstance(action, str):
                return action
            else:
                return ''

        out = ''
        # actions = [str(a) if isinstance(a, int) else a for a in actions]
        print(f'Enlarging {symbol_in}')

        for char, action in zip(symbol_in, actions):
            outout = resolve_int_or_str(action, char)
            if outout:
                out += outout
            elif isinstance(action, dict):
                for k, v in action.items():
                    if re.match(k, char):  # TODO Fullmatch
                        out += resolve_int_or_str(v, char)

        return out

    @staticmethod
    def shorten(symbol_in: str = '', actions: list = [],
                encoding: str = 'semantic') -> str:
        """Shortenes symbol split with r'.-_'.

        Encoding is set for semantic or agnostic.
        Actions is list of instructions for individual parts of symbol.
        Options are:
            0 - leave it as is
            1 - shorten to only the first char
            2 - shorten to first two chars
            -1 - shorten to only last char
            9 - ignore part
            r'[0129]sep' - same as previos but add seperator at the end

        All lowercase if encoding is semantic,
            uppercase if encoding is agnostic.
        """
        def resolve_int(action: int, _input: str):
            if action == 0:
                return _input
            elif action == 1 and len(_input) > 0:
                return _input[0]
            elif action == 2 and len(_input) > 1:
                return _input[:2]
            elif action == -1 and len(_input) > 0:
                return _input[-1]
            else:
                print('AAAAAAAAA')
                print(type(action))
        out = ''
        # actions = [str(a) if isinstance(a, int) else a for a in actions]
        print(symbol_in)

        parts = re.split(r'\.|\-|\_', symbol_in)
        for part, action in zip(parts, actions):
            if isinstance(action, int):
                out += resolve_int(action, part)
            elif isinstance(action, str):
                if re.fullmatch(r'\d', action[0]):
                    out += resolve_int(int(action[0]), part)
                    if len(action) > 3 and action[1:] == 'sep':
                        out += Symbol_converter.SEPARATOR

        if out[-1] == Symbol_converter.SEPARATOR:
            out = out[:-1]

        if encoding == 'semantic':
            out = out.lower()
        elif encoding == 'agnostic':
            out = out.upper()

        print(f'OUT: {out}')
        return out

    converting_patterns_back = {
        'b': 'barline',
        'B': 'barline-L1',
        'C[CFG]\d':
            partial(enlarge.__func__,
                    actions=['clef.', {c: f'{c}-' for c in 'CFG'},
                             {str(d): f'L{d}' for d in range(10)}]),
        'DS'+SEPARATOR+r'?\d':
            partial(enlarge.__func__,
                    actions=['dot-', 'S', {SEPARATOR: '-', r'\d': 0}, 0]),
        'F': 'fermata.above-S6',


        'S(S|E)(L|S)'+SEPARATOR+r'?\d':
            partial(enlarge.__func__,
                    actions=['slur.', {'E': 'end-', 'S': 'start-'}, 0,
                             {SEPARATOR: '-', r'\d': 0}, 0])
    }

    converting_patterns = {
        'barline': 'b',
        'barline-L1': 'B',
        'clef\.[CFG]-L\d':
            partial(shorten.__func__, actions=[1, 1, -1], encoding='agnostic'),
        'dot-S[-\d]{1,2}':
            partial(shorten.__func__, actions=[1, '0sep', 0],
                    encoding='agnostic'),
        'fermata.above-S6': 'F',

        'slur.(start|end)-\S*':
            partial(shorten.__func__, actions=[1, 1, '0sep', 0],
                    encoding='agnostic')
    }

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
    def convert_list(symbols_in: list = [], reverse: bool = False) -> list:
        symbols_out = []
        for sym in symbols_in:
            symbols_out.append(Symbol_converter.convert(sym, reverse=reverse))
        return symbols_out

    @staticmethod
    def convert(symbol: str = '', reverse: bool = False) -> str:
        """Convert symbol and back.

        if Direction is True, convert to smaller
        else convert to larger.
        """

        if reverse:
            pattern_matching = Symbol_converter.converting_patterns_back
        else:
            pattern_matching = Symbol_converter.converting_patterns

        out = ''
        for k, v in pattern_matching.items():
            if re.fullmatch(k, symbol):  # TODO fullmatch
                if isinstance(v, str):
                    out = v
                else:
                    out = v(symbol_in=symbol)
                break

        print(f'[CONVERT] OUT: {out}')
        return out


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
