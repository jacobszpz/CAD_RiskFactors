#!/usr/bin/env python3

import argparse
from dataset import Dataset

def main() -> int:
    parser = argparse.ArgumentParser(
            description='Iterate over files in a folder')

    parser.add_argument('folder', type=str, help='the path to the folder')

    args = parser.parse_args()

    # get the path to the folder from the parsed arguments
    data = Dataset(args.folder)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

