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
    SEPARATORS = r'[\-\.\_]'

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
    def _resolve_action(action: any, _input: str = '') -> str:
        def resolve_int(action: any, _input: str) -> str:
            if action == 0:
                return _input
            elif action == 1 and len(_input) > 0:
                return _input[0]
            elif action == 2 and len(_input) > 1:
                return _input[:2]
            elif action == -1 and len(_input) > 0:
                return _input[-1]
            else:
                raise ValueError(f'Int convert action of unexpected value '
                                 f'({action}) on input {_input}')

        def resolve_int_or_str(action: any, _input: str) -> str:
            if isinstance(action, int):
                return resolve_int(action, _input)
            elif isinstance(action, str):
                if re.fullmatch(r'-?\dsep', action):
                    int_action = int(re.split('sep', action)[0])
                    resolved = resolve_int(int_action, _input)
                    return resolved + Symbol_converter.SEPARATOR
                else:
                    return action
            return ''

        if isinstance(action, int) or isinstance(action, str):
            return resolve_int_or_str(action, _input)
        elif isinstance(action, dict):
            for k, v in action.items():
                if re.fullmatch(k, _input):
                    return resolve_int_or_str(v, _input)
        return None  # Should cause error

    @staticmethod
    def enlarge(symbol_in: str = '', actions: list = []):
        """Enlarge symbol back to original encoding

        Actions is list of instructions for individual chars of symbol.
        Options are:
            0 - leave it as is
            str - place string instead of original char
            dict - find first key that matches and and do the action in value
                 - actions inside values are the same as above
        """
        print(f'IN: {symbol_in}')
        out = ''
        for char, action in zip(symbol_in, actions):
            out += Symbol_converter._resolve_action(action, char)
        print(f'[LONGER] OUT: {out}')
        return out

    @staticmethod
    def shorten(symbol_in: str = '', actions: list = [],
                encoding: str = 'semantic',
                separators: str = SEPARATORS) -> str:
        """Shortenes symbol split with `Symbol_converter.SEPARATORS`.

        Encoding is set for semantic or agnostic.
        Actions is list of instructions for individual parts of symbol.
        Options are:
            0 - leave it as is
            1 - shorten to only the first char
            2 - shorten to first two chars
            -1 - shorten to only last char
            r'[012]sep' - same as previos but add seperator at the end
            dict - find first key that matches and and do the action in value
                 - actions inside values are the same as above

        All lowercase if encoding is semantic,
            uppercase if encoding is agnostic.
        """
        print(f'IN: {symbol_in}')
        out = ''

        parts = re.split(separators, symbol_in)
        for part, action in zip(parts, actions):
            out += Symbol_converter._resolve_action(action, part)

        if out[-1] == Symbol_converter.SEPARATOR:
            out = out[:-1]

        if encoding == 'semantic':
            out = out.lower()
        elif encoding == 'agnostic':
            out = out.upper()

        print(f'[SHORTER] OUT: {out}')
        return out

    conv_patt_back = {  # Converting patterns BACK
        # agnostic accidental
        r'A[FNS][LS]\d':
            partial(enlarge.__func__,
                    actions=['accidental.',
                             {'F': 'flat-', 'N': 'natural-', 'S': 'sharp-'},
                             0, 0]),
        r'A[FNS][LS]'+SEPARATOR+r'\d':
            partial(enlarge.__func__,
                    actions=['accidental.',
                             {'F': 'flat-', 'N': 'natural-', 'S': 'sharp-'},
                             0, '-', 0]),
        # agnostic clefs
        r'C[CFG]\d':
            partial(enlarge.__func__,
                    actions=['clef.', {c: f'{c}-' for c in 'CFG'},
                             {str(d): f'L{d}' for d in range(10)}]),
        # agnostic digits
        r'D\d[HLS]':
            partial(enlarge.__func__, actions=[
                'digit.', 0, {'H': '-L4', 'L': '-L2', 'S': '-S5'}]),
        r'D\d{2}[HLS]':
            partial(enlarge.__func__, actions=[
                'digit.', 0, 0, {'H': '-L4', 'L': '-L2', 'S': '-S5'}]),
        # agnostic dots
        'DS'+SEPARATOR+r'?\d':
            partial(enlarge.__func__,
                    actions=['dot-', 'S', {SEPARATOR: '-', r'\d': 0}, 0]),
        # semantic multirest
        r'm\d{1,4}':
            partial(enlarge.__func__, actions=['multirest-', 0, 0, 0, 0]),
        # agnostic rest
        r'R[EHQSTW46]\d':
            partial(enlarge.__func__,
                    actions=['rest.',
                             {'E': 'eighth', 'H': 'half',
                              'Q': 'quadruple_whole', 'S': 'sixty_fourth',
                              'T': 'thirty_second', 'W': 'whole',
                              '4': 'quarter', '6': 'sixteenth'},
                             {str(d): f'-L{d}' for d in range(10)}]),

        # agnostic slur
        r'S(S|E)(L|S)\d':
            partial(enlarge.__func__,
                    actions=['slur.', {'E': 'end-', 'S': 'start-'}, 0, 0]),
        r'S(S|E)(L|S)'+SEPARATOR+r'\d':
            partial(enlarge.__func__,
                    actions=['slur.', {'E': 'end-', 'S': 'start-'}, 0, '-', 0])
    }

    simple_conv_patt = {}

    conv_patt = {   # Converting patterns
        r'accidental\.(flat|natural|sharp)-[SL]-?\d':
            partial(shorten.__func__, actions=[1, 1, '0sep', 0],
                    encoding='agnostic'),
        'barline': 'b',
        'barline-L1': 'B',
        r'clef\.[CFG]-L\d':
            partial(shorten.__func__, actions=[1, 1, -1], encoding='agnostic'),
        r'digit\.\d{1,2}-(S5|L2|L4)':
            partial(shorten.__func__, encoding='agnostic',
                    actions=[1, 0, {'L2': 'L', 'L4': 'H', 'S5': 1}]),
        r'dot-S[-\d]{1,2}':
            partial(shorten.__func__, actions=[1, '0sep', 0],
                    encoding='agnostic'),
        'fermata.above-S6': 'F',
        'metersign.C-L3': 'MC',
        'metersign.C/-L3': 'MD',
        'multirest-L3': 'M',
        r'multirest-\d{1,4}':
            partial(shorten.__func__, actions=[1, 0]),
        r'rest\.[a-z_]+-L\d':
            partial(shorten.__func__,
                    actions=[1, {'quarter': '4', 'sixteenth': '6',
                                 r'[ehqstw]\S+': 1}, -1],
                    encoding='agnostic', separators=r'[\.\-]'),

        r'slur.(start|end)-\S*':
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
        if len(Symbol_converter.simple_conv_patt) == 0:
            print(f'len(conv_patt_back): '
                  f'{len(Symbol_converter.conv_patt_back)}')
            simple_conv_patt = {
                v: k for k, v in Symbol_converter.conv_patt.items()
                if isinstance(k, str) and isinstance(v, str)
            }
            Symbol_converter.conv_patt_back.update(simple_conv_patt)
            Symbol_converter.simple_conv_patt = simple_conv_patt
            print(f'len(conv_patt_back): '
                  f'{len(Symbol_converter.conv_patt_back)}')

        if reverse:
            pattern_matching = Symbol_converter.conv_patt_back
        else:
            pattern_matching = Symbol_converter.conv_patt

        out = ''
        for k, v in pattern_matching.items():
            if re.fullmatch(k, symbol):
                if isinstance(v, str):
                    out = v
                else:
                    out = v(symbol_in=symbol)
                break
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
