"""Download flags of top 20 countries by population

ThreadPoolExecutor version

Sample run::

    $ python3 flags_threadpool.py
    DE FR BD CN EG RU IN TR VN ID JP BR NG MX PK ET PH CD US IR
    20 downloads in 0.35s

"""
# BEGIN FLAGS_THREADPOOL
import os
import time
from concurrent import futures  # <1>

import urllib.request

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'http://flupy.org/data/flags'

DEST_DIR = 'downloaded/'

MAX_WORKERS = 20  # <2>


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):
    cc = cc.lower()
    url = f'{BASE_URL}/{cc}/{cc}.gif'
    resp = urllib.request.urlopen(url)
    return resp.read()


def download_one(cc):  # <3>
    image = get_flag(cc)
    print(cc, end=' ', flush=True)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))               # <4>
    with futures.ThreadPoolExecutor(workers) as executor:  # <5>
        res = executor.map(download_one, sorted(cc_list))  # <6>

    return len(list(res))                                  # <7>


def main():  # <8>
    t0 = time.perf_counter()
    count = download_many(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')


if __name__ == '__main__':
    main()
# END FLAGS_THREADPOOL
