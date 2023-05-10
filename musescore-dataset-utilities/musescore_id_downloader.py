#!/usr/bin/python3.8
"""Downloads IDs of all OPEN DOMAIN musescore files from musescore forum."""

import argparse
import re
import os
import time
import requests


class ID_downloader:
    @staticmethod
    def download_IDs(database: str = ''):
        url = 'https://musescore.com/sheetmusic?complexity=2&page='

        ids = ID_downloader.read_database(database)

        for page in range(1, 100):
            print(f'page: {page}')
            old_len = len(ids)
            html = ID_downloader.download_html(
                f'{url}{page}&recording_type=public-domain&'
                'sort=rating&type=non-official')
            ids += ID_downloader.strip_ids(html)
            ids = list(set(ids))
            new_len = len(ids)

            print(f'old ids len: {old_len}, new ids len: {new_len}')

            page += 1

        print(f'Found {len(ids)} unique IDs.')
        return ids

    @staticmethod
    def download_html(url: str):
        output = requests.get(url, timeout=10).text
        return output

    @staticmethod
    def strip_ids(html: str = ''):
        ids = re.findall(r'user/\d+/scores/\d+', html)
        ids = list(set(ids))
        return ids

    @staticmethod
    def read_database(file: str = ''):
        if not file or not os.path.isfile(file):
            return []

        with open(file, encoding='utf-8') as f:
            data = f.read()
        ids = re.split(r'\n', data)
        print(f'loaded {len(ids)} ids from DB')
        return ids

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', "--output-file", default='stdout', required=False,
        help="Output file where to write list of all IDs")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    ids = ID_downloader.download_IDs(database = args.output_file)
    if args.output_file == 'stdout':
        print('======================== Printing all IDs.')
        print(ids)
        print('========================')
    else:
        print(f'Printing IDs to {args.output_file}')
        output = '\n'.join(sorted(ids))
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(output)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
