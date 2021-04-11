#!/usr/bin/env python3
import argparse
import sys
from page_loader import download


def main():
    parser = argparse.ArgumentParser(description='page loader')
    parser.add_argument('url', type=str)

    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='set output directory')

    args = parser.parse_args()

    if args.output is not None and args.url is not None:
        try:
            print(download(args.url, args.output))
        except Exception:
            sys.exit()
    else:
        print(args.accumulate(args.integers))


if __name__ == '__main__':
    main()
