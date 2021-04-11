#!/usr/bin/env python3
import argparse
import logging
import sys
from page_loader import download

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def main():
    parser = argparse.ArgumentParser(description='page loader')
    parser.add_argument('url', type=str)

    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='set output directory')

    args = parser.parse_args()
    logger.debug(f'args: {args}')

    if args.output is not None and args.url is not None:
        print(download(args.url, args.output))
    else:
        print(args.accumulate(args.integers))


if __name__ == '__main__':
    main()
