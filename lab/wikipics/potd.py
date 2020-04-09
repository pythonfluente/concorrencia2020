#!/usr/bin/env python3

'''Get URLs for Wikipedia's collection of "Pictures of The Day"'''

import collections
import math
import random
from urllib import parse
import pathlib


BASE_URL = 'https://upload.wikimedia.org/wikipedia/commons/'
LOCAL_PATH = 'img/'
PICS_FILE = 'pictures.txt'

DEFAULT_TARGET_SIZE = 4_000_000
TOLERANCE = .05


def file_name(url):
    url_parts = parse.urlsplit(url)
    path = pathlib.PurePath(url_parts.path)
    return path.parts[-1]


def save(url, octets):
    name = file_name(url)
    save_path = LOCAL_PATH + name 
    with open(save_path, 'wb') as fp:
        fp.write(octets)
    return name


def pick_by_size(target_size):
    selected = filter_by_size(target_size)
    return random.choice(selected)


def filter_by_size(target_size, *, include_size=False):
    with open(PICS_FILE) as fp:
        for line in fp:
            size_field, path = line.strip().split()
            size = int(size_field)
            if math.isclose(target_size, size, rel_tol=TOLERANCE):
                if include_size:
                    yield (size, path)
                else:
                    yield path


def main(args):
    if '-s' in args:
        args.remove('-s')
        include_size = True
    else:
        include_size = False
    if len(args) == 1:
        target_size = float(args[0])
    else:
        target_size = DEFAULT_TARGET_SIZE
        
    for item in filter_by_size(target_size, include_size=include_size):
        if include_size:
            size, path = item
            print(f'{size:_d}\t {path}')
        else:
            print(item)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])