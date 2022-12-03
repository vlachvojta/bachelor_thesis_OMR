#!/usr/bin/python3.8

import re
import json
from symbol_converter import Symbol_converter


def main():

    _input = input()

    symbols = json.loads(_input)

    out = []
    for symbol in symbols:
        out.append(Symbol_converter.convert(symbol, to_smaller=False))

    print('====================')
    print(json.dumps(out))


if __name__ == '__main__':
    main()
