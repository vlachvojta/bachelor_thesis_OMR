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
    def _reverse_dict(data: dict = {}) -> dict:
        new = {}
        for k, v in data.items():
            if v in list(new.keys()) and len(k) > len(new[v]):
                new[v] = k
            else:
                new.update({v: k})
        return new
        # return {v: k for k, v in data.items()}

    @staticmethod
    def _resolve_int_action(action: any, _input: str) -> str:
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

    @staticmethod
    def _resolve_int_or_str_action(action: any, _input: str) -> str:
        if isinstance(action, int):
            return Symbol_converter._resolve_int_action(action, _input)
        elif isinstance(action, str):
            if action == '':
                return ''
            if re.fullmatch(r'-?\d(sep|up|low)', action):
                int_action = int(re.split(r'(sep|up|low)', action)[0])
                out = Symbol_converter._resolve_int_action(int_action,
                                                           _input)
                str_action = re.split(r'\d', action)[-1]
                if str_action == 'sep':
                    return out + Symbol_converter.SEPARATOR
                elif str_action == 'up':
                    return out.upper()
                elif str_action == 'low':
                    return out.lower()
                else:
                    return out
            else:
                return action
        return ''

    @staticmethod
    def _resolve_action(action: any, _input: str = '') -> str:
        # debug_mode = False
        # if _input == 'rest-eighth.': debug_mode = True
        print(f'action: {action}, input: {_input}', flush=True)
        if isinstance(action, int) or isinstance(action, str):
            return Symbol_converter._resolve_int_or_str_action(action, _input)
        elif isinstance(action, dict):
            for k, v in action.items():
                if re.fullmatch(k, _input) or k == '':
                    return Symbol_converter._resolve_int_or_str_action(
                        v, _input)
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
        # print(f'IN: {symbol_in}')
        out = ''
        for char, action in zip(symbol_in, actions):
            out += Symbol_converter._resolve_action(action, char)
        # print(f'[LONGER] OUT: {out}')
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
        print(f'\nIN: {symbol_in}')
        out = ''

        parts = re.split(separators, symbol_in)
        for part, action in zip(parts, actions):
            print(f'part: {part}, action: {action}')
            out += Symbol_converter._resolve_action(action, part)

        if out[-1] == Symbol_converter.SEPARATOR:
            out = out[:-1]

        if encoding == 'semantic':
            out = out.lower()
        elif encoding == 'agnostic':
            out = out.upper()

        # print(f'[SHORTER] OUT: {out}')
        return out

    length_dict = {
        'double': 'D', 'double_whole': 'D', 'eighth': 'E', 'half': 'H',
        'quadruple': 'Q', 'quadruple_whole': 'Q', 'sixty': 'S',
        'sixty_fourth': 'S', 'thirty': 'T', 'thirty_second': 'T',
        'whole': 'W', 'quarter': '4', 'sixteenth': '6'}
    length_dict_back = _reverse_dict.__func__(length_dict)

    length_keys_list = '(' + '|'.join(list(length_dict.keys())) + ')'
    length_values_list = '(' + '|'.join(list(length_dict.values())) + ')'

    length_inits_dict = {
        'double': 'D', 'eighth': 'E', 'half': 'H', 'quadruple': 'Q',
        'sixty': 'S', 'thirty': 'T', 'whole': 'W', 'quarter': '4',
        'sixteenth': '6'}

    length_tails = ['whole', 'fourth', 'second']

    other_part_length_or_dot = {v: ('.' if v == '' else '')
                                for v in length_tails+['']}
    other_part_length_or_fer = {v: ('f' if v == 'fermata' else '')
                                for v in length_tails+['fermata']}
    fer_or_dot = {'fermata': 1, '': '.'}

    conv_patt_str = {   # Converting patterns strings
        'barline': 'b',
        'barline-L1': 'B',
        'fermata.above-S6': 'F',
        'metersign.C-L3': 'MC',
        'metersign.C/-L3': 'MD',
        'multirest-L3': 'M',
        'tie': 't',
        "rest-eighth": 're',
        "rest-eighth.": 're.',
        "rest-eighth..": 're..',
        "rest-eighth._fermata": 're.f',
        "rest-eighth_fermata": 'ref',
        "rest-half": 'rh',
        "rest-half.": 'rh.',
        "rest-half._fermata": 'rh.f',
        "rest-half_fermata": 'rhf',
        "rest-quadruple_whole": 'rq',
        "rest-quarter": 'r4',
        "rest-quarter.": 'r4.',
        "rest-quarter..": 'r4..',
        "rest-quarter.._fermata": 'r4..f',
        "rest-quarter._fermata": 'r4.f',
        "rest-quarter_fermata": 'r4f',
        "rest-sixteenth": 'r6',
        "rest-sixteenth.": 'r6.',
        "rest-sixteenth_fermata": 'r6f',
        "rest-sixty_fourth": 'rs',
        "rest-thirty_second": 'rt',
        "rest-whole": 'rw',
        "rest-whole.": 'rw.',
        "rest-whole_fermata": 'rwf'}

    conv_patt_reg = {   # Converting patterns with regexes
        r'accidental\.(flat|natural|sharp)-[SL]-?\d':
            partial(shorten.__func__, actions=[1, 1, '0sep', 0],
                    encoding='agnostic'),
        r'clef-[CFG]\d':    # semantic clef
            partial(shorten.__func__, actions=[1, 0]),
        r'clef\.[CFG]-L\d':  # agnostic clef
            partial(shorten.__func__, actions=[1, 1, -1], encoding='agnostic'),
        r'digit\.\d{1,2}-(S5|L2|L4)':
            partial(shorten.__func__, encoding='agnostic',
                    actions=[1, 0, {'L2': 'L', 'L4': 'H', 'S5': 1}]),
        r'dot-S[-\d]{1,2}':
            partial(shorten.__func__, actions=[1, '0sep', 0],
                    encoding='agnostic'),
        r'gracenote\.beamedBoth\d-[LS]-?\d':
            partial(shorten.__func__, encoding='agnostic',
                    actions=[1, {f'beamedBoth{i}': f'B{i}' for i in range(10)},
                             '0sep', 0]),
        r'gracenote\.beamedRight\d-[LS]-?\d':
            partial(shorten.__func__, encoding='agnostic',
                    actions=[1,
                             {f'beamedRight{i}': f'R{i}' for i in range(10)},
                             '0sep', 0]),
        r'gracenote\.(' + length_keys_list + r')-[LS]-?\d':
            partial(shorten.__func__, encoding='agnostic',
                    actions=[1, length_dict, '0sep', 0],
                    separators=r'[\.\-]'),
        r'keySignature-[A-G][#b]?M':
            partial(shorten.__func__, actions=[1, 0]),
        r'note\.beamedBoth\d-[LS]-?\d':
            partial(shorten.__func__, encoding='agnostic',
                    actions=[1, {f'beamedBoth{i}': f'B{i}' for i in range(10)},
                             '0sep', 0]),
        r'note\.beamedRight\d-[LS]-?\d':
            partial(shorten.__func__, encoding='agnostic',
                    actions=[1,
                             {f'beamedRight{i}': f'R{i}' for i in range(10)},
                             '0sep', 0]),
        r'note\.beamedLeft\d-[LS]-?\d':
            partial(shorten.__func__, encoding='agnostic',
                    actions=[1, {f'beamedLeft{i}': f'L{i}' for i in range(10)},
                             '0sep', 0]),
        r'note\.(' + length_keys_list + r')-[LS]-?\d':
            partial(shorten.__func__, actions=[1, length_dict, '0sep', 0],
                    encoding='agnostic', separators=r'[\.\-]'),

        r'multirest-\d{1,4}':
            partial(shorten.__func__, actions=[1, 0]),
        # r'rest-(eighth|half|quadruple_whole|quarter|sixteenth|sixty|thirty_second|whole)\.{0,2}(_fermata)?':
        # semantic rest
        # r'rest-' + length_keys_list + r'\.(_fermata)?':
        # r'rest-' + length_keys_list + r'\.{0,2}(_fermata)?':
        #     partial(
        #         shorten.__func__, separators=r'[\-\_\.]',
        #         actions=[1, length_dict, other_part_length_or_dot,
        #                  [fer_or_dot] * 3]),
        # r'rest-' + length_keys_list + r'(_fermata)?':
        #     partial(
        #         shorten.__func__, separators=r'[\-\_\.]',
        #         actions=[1, length_dict, other_part_length_or_fer, 1]),
        # r'rest-' + length_keys_list + r'\.\.(_fermata)?':
        #     partial(
        #         shorten.__func__, separators=r'[\-\_\.]',
        #         actions=[
        #             1, length_dict, {v: '' for v in length_tails}, {'': '.'},
        #             '.', {'fermata': 1, '': '.'}, 1]),
        # agnostic rest
        r'rest\.' + length_keys_list + r'-L\d':
            partial(shorten.__func__,
                    actions=[1, length_dict, -1],
                    encoding='agnostic', separators=r'[\.\-]'),

        r'slur.(start|end)-\S*':
            partial(shorten.__func__, actions=[1, 1, '0sep', 0],
                    encoding='agnostic')
    }

    conv_patt_back_str = {
        v: k for k, v in conv_patt_str.items()}

    conv_patt_back_reg = {  # Converting patterns BACK
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
        # semantic clefs
        r'c[cfg]\d':
            partial(enlarge.__func__, actions=['clef-', '0up', 0]),
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
        # agnostic gracenote
        r'G[RB]\d[SL]_?\d':
            partial(enlarge.__func__,
                    actions=['gracenote.',
                             {'R': 'beamedRight', 'B': 'beamedBoth'}, 0,
                             {'S': '-S', 'L': '-L'},
                             {SEPARATOR: '-', r'\d': 0}, 0]),
        r'G[' + length_values_list + r'][SL]_?\d':
            partial(
                enlarge.__func__,
                actions=[
                    'gracenote.',
                    length_dict_back,
                    {'S': '-S', 'L': '-L'}, {SEPARATOR: '-', r'\d': 0}, 0]),
        # semantic keySignature
        r'k[a-g]m':
            partial(enlarge.__func__, actions=['keySignature-', '0up', '0up']),
        r'k[a-g][#b]m':
            partial(enlarge.__func__,
                    actions=['keySignature-', '0up', 0, '0up']),
        # agnostic note
        r'N[RBL]\d[SL]_?\d':
            partial(enlarge.__func__,
                    actions=['note.',
                             {'R': 'beamedRight', 'B': 'beamedBoth',
                              'L': 'beamedLeft'}, 0,
                             {'S': '-S', 'L': '-L'},
                             {SEPARATOR: '-', r'\d': 0}, 0]),
        r'N[' + length_values_list + r'][SL]_?\d':
            partial(
                enlarge.__func__,
                actions=[
                    'note.',
                    length_dict_back,
                    {'S': '-S', 'L': '-L'}, {SEPARATOR: '-', r'\d': 0}, 0]),

        # semantic multirest
        r'm\d{1,4}':
            partial(enlarge.__func__, actions=['multirest-', 0, 0, 0, 0]),
        # agnostic rest
        r'R[' + length_values_list + r']\d':
            partial(enlarge.__func__,
                    actions=['rest.', length_dict_back,
                             {str(d): f'-L{d}' for d in range(10)}]),

        # agnostic slur
        r'S(S|E)(L|S)\d':
            partial(enlarge.__func__,
                    actions=['slur.', {'E': 'end-', 'S': 'start-'}, 0, 0]),
        r'S(S|E)(L|S)'+SEPARATOR+r'\d':
            partial(enlarge.__func__,
                    actions=['slur.', {'E': 'end-', 'S': 'start-'}, 0, '-', 0])
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
        print(f'IN: {symbol}')
        if len(Symbol_converter.conv_patt_back_str) == 0:
            Symbol_converter.conv_patt_back_str = {
                v: k for k, v in Symbol_converter.conv_patt_str.items()}

        if reverse:
            pattern_matching_str = Symbol_converter.conv_patt_back_str
            pattern_matching_reg = Symbol_converter.conv_patt_back_reg
        else:
            pattern_matching_str = Symbol_converter.conv_patt_str
            pattern_matching_reg = Symbol_converter.conv_patt_reg

        if symbol in list(pattern_matching_str.keys()):
            print('\tFound match in str')
            return pattern_matching_str[symbol]

        for k, v in pattern_matching_reg.items():
            if re.fullmatch(k, symbol):
                return v(symbol_in=symbol)


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
