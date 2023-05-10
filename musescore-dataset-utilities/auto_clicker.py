#!/usr/bin/python3.8
"""Simple script to automate clicking at the same spot on the screen every time.

Used for automating the MuseScore Batch Convert when it was prompting about saving every file.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import time
import argparse

import pyautogui as pg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--number-of-clicks", type=int, default=10,
        help="Number of times to click on the screen")
    parser.add_argument(
        "-X", type=int, default=940,
        help="X position of click")
    parser.add_argument(
        "-Y", type=int, default=555,
        help="Y position of click")
    parser.add_argument(
        "-s", '--sleep', type=int, default=10,
        help="Sleep between clicks in seconds.")
    args = parser.parse_args()

    time.sleep(5)   # Wait before starting

    for i in range(args.number_of_clicks):
        print(i)
        pg.click(args.X, args.Y)
        pg.click(args.X, 0)
        time.sleep(args.sleep)


if __name__ == "__main__":
    main()
