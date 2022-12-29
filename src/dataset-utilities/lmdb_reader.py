#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


import lmdb


def read_lmdb_key_from_file(file: str, key: str):
    lmdb_env = lmdb.open(file)

    with lmdb_env.begin() as txn:
        with txn.cursor() as curs:
            print(f'Reading key ({key}) from file ({file})')
            print(curs.get(key.encode()))
            # For decoding byte sings use: 
            # print(curs.get(key.encode()).decode())


def main():
    FILE_NAME = '../../../datasets/primus_subset_converted_lmdb/1.lmdb'
    LMDB_KEY = '000001-000000.semantic'
    read_lmdb_key_from_file(FILE_NAME, LMDB_KEY)


if __name__ == '__main__':
    main()
