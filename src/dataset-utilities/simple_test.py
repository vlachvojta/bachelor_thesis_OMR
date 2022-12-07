#!/usr/bin/python3.8

import re
import json
from symbol_converter import Symbol_converter


def main():

    # _input = input()
    # symbols = json.loads(_input)
    symbols_ll = [
        ["dot-S-1", "dot-S-2", "dot-S-3", "dot-S0", "dot-S1", "dot-S2", "dot-S3", "dot-S4", "dot-S5", "dot-S6", "dot-S7", "dot-S8"],
        ["barline-L1", 'barline', "fermata.above-S6"],
        ["slur.end-L-1", "slur.end-L-2", "slur.end-L0", "slur.end-L1", "slur.end-L2", "slur.end-L3", "slur.end-L4", "slur.end-L5", "slur.end-L6", "slur.end-L7", "slur.end-L8", "slur.end-S-1", "slur.end-S-2", "slur.end-S0", "slur.end-S1", "slur.end-S2", "slur.end-S3", "slur.end-S4", "slur.end-S5", "slur.end-S6", "slur.end-S7", "slur.start-L-1", "slur.start-L-2", "slur.start-L0", "slur.start-L1", "slur.start-L2", "slur.start-L3", "slur.start-L4", "slur.start-L5", "slur.start-L6", "slur.start-L7", "slur.start-L8", "slur.start-S-1", "slur.start-S-2", "slur.start-S0", "slur.start-S1", "slur.start-S2", "slur.start-S3", "slur.start-S4", "slur.start-S5", "slur.start-S6", "slur.start-S7"],
        ["clef.C-L1", "clef.C-L2", "clef.C-L3", "clef.C-L4", "clef.C-L5", "clef.F-L3", "clef.F-L4", "clef.F-L5", "clef.G-L1", "clef.G-L2"],
        ["multirest-1", "multirest-10", "multirest-100", "multirest-105", "multirest-107", "multirest-11", "multirest-1111", "multirest-112", "multirest-115", "multirest-119", "multirest-12", "multirest-123", "multirest-124", "multirest-126", "multirest-128", "multirest-13", "multirest-14", "multirest-143", "multirest-15", "multirest-16", "multirest-164", "multirest-17", "multirest-18", "multirest-19", "multirest-193", "multirest-2", "multirest-20", "multirest-21", "multirest-22", "multirest-225", "multirest-23", "multirest-24", "multirest-25", "multirest-26", "multirest-27", "multirest-28", "multirest-29", "multirest-3", "multirest-30", "multirest-31", "multirest-32", "multirest-33", "multirest-34", "multirest-35", "multirest-36", "multirest-37", "multirest-38", "multirest-39", "multirest-4", "multirest-40", "multirest-41", "multirest-42", "multirest-43", "multirest-44", "multirest-45", "multirest-46", "multirest-47", "multirest-48", "multirest-49", "multirest-5", "multirest-50", "multirest-51", "multirest-52", "multirest-53", "multirest-54", "multirest-55", "multirest-56", "multirest-57", "multirest-58", "multirest-59", "multirest-6", "multirest-60", "multirest-63", "multirest-64", "multirest-65", "multirest-66", "multirest-67", "multirest-68", "multirest-69", "multirest-7", "multirest-70", "multirest-71", "multirest-72", "multirest-73", "multirest-76", "multirest-77", "multirest-79", "multirest-8", "multirest-80", "multirest-81", "multirest-88", "multirest-89", "multirest-9", "multirest-91", "multirest-94", "multirest-96", "multirest-98", "multirest-99"],
        ["rest.eighth-L3", "rest.half-L3", "rest.quadruple_whole-L3", "rest.quarter-L3", "rest.sixteenth-L3", "rest.sixty_fourth-L3", "rest.thirty_second-L3", "rest.whole-L4"],

        ["multirest-L3"],
        ["metersign.C-L3", "metersign.C/-L3"]
        ]

    symbols = [item for sublist in symbols_ll for item in sublist]

    shorter = Symbol_converter.convert_list(symbols)
    longer = Symbol_converter.convert_list(shorter, reverse=True)



    if longer == symbols:
        shorter_ll = []
        for i, sublist in enumerate(symbols_ll):
            if len(sublist) >= 5:
                symbols_ll[i] = sublist[:5]
                sublist = sublist[:5]
            shorter_ll.append(Symbol_converter.convert_list(sublist))
        print('================================')
        print('HUURAAA, it works both ways.')
        print('================================')
        for syms, short in zip(symbols_ll, shorter_ll):
            print(f'{syms}:')
            print(f'\t{short}')
    else:
        print('================================')
        print('IT DOES NNOT...')
        print('================================')
        sym_err = []
        short_err = []
        long_err = []
        for sym, short, long in zip(symbols, shorter, longer):
            if not sym == long:
                sym_err.append(sym)
                short_err.append(short)
                long_err.append(long)

        print("Different symbols:")
        print(f'input: {sym_err}')
        print(f'shorter: {short_err}')
        print(f'longer: {long_err}')


if __name__ == '__main__':
    main()
