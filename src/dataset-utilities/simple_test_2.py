#!/usr/bin/python3.8

import re
import json
from symbol_converter import Symbol_converter
from common import Common


def main():
    sc = Symbol_converter()
    print(type(sc))

    file = Common.read_file('230006612-1_2_2.semantic')
    file = re.split(r'\s', file)
    print(type(file))
    print(' '.join(sc.convert_list(file)))


if __name__ == '__main__':
    main()
