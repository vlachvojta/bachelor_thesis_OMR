#!/usr/bin/python3.8

import re
import json
from symbol_converter import Symbol_converter


def main():

    # _input = input()
    # symbols = json.loads(_input)
    symbols = [
        "dot-S-1", "dot-S-2", "dot-S-3", "dot-S0", "dot-S1", "dot-S2", "dot-S3", "dot-S4", "dot-S5", "dot-S6", "dot-S7", "dot-S8",
        "barline-L1", 'barline', "fermata.above-S6",
        "slur.end-L-1", "slur.end-L-2", "slur.end-L0", "slur.end-L1", "slur.end-L2", "slur.end-L3", "slur.end-L4", "slur.end-L5", "slur.end-L6", "slur.end-L7", "slur.end-L8", "slur.end-S-1", "slur.end-S-2", "slur.end-S0", "slur.end-S1", "slur.end-S2", "slur.end-S3", "slur.end-S4", "slur.end-S5", "slur.end-S6", "slur.end-S7", "slur.start-L-1", "slur.start-L-2", "slur.start-L0", "slur.start-L1", "slur.start-L2", "slur.start-L3", "slur.start-L4", "slur.start-L5", "slur.start-L6", "slur.start-L7", "slur.start-L8", "slur.start-S-1", "slur.start-S-2", "slur.start-S0", "slur.start-S1", "slur.start-S2", "slur.start-S3", "slur.start-S4", "slur.start-S5", "slur.start-S6", "slur.start-S7",
        "clef.C-L1", "clef.C-L2", "clef.C-L3", "clef.C-L4", "clef.C-L5", "clef.F-L3", "clef.F-L4", "clef.F-L5", "clef.G-L1", "clef.G-L2"
        ]

    shorter = Symbol_converter.convert_list(symbols)
    longer = Symbol_converter.convert_list(shorter, reverse=True)

    print('====================')

    if longer == symbols:
        print('HUURAAA, it works both ways.')
        print(shorter)
    else:
        print('IT DOES NNOT...')
        print(f'shorter: {shorter}')
        print(f'longer: {longer}')


if __name__ == '__main__':
    main()
