"""Download flags of top 20 countries by population

Sequential version

Sample run::

    $ python3 flags.py
    BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN
    20 downloads in 5.49s

"""
# BEGIN FLAGS_PY
import os
import time

import urllib.request  # <1>

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()  # <2>

BASE_URL = 'http://flupy.org/data/flags'  # <3>

DEST_DIR = 'downloaded/'  # <4>


def save_flag(img, filename):  # <5>
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):  # <6>
    cc = cc.lower()
    url = f'{BASE_URL}/{cc}/{cc}.gif'
    resp = urllib.request.urlopen(url)
    return resp.read()


def download_many(cc_list):  # <7>
    for cc in sorted(cc_list):  # <8>
        image = get_flag(cc)
        print(cc, end=' ', flush=True)
        save_flag(image, cc.lower() + '.gif')

    return len(cc_list)


def main():  # <9>
    t0 = time.perf_counter()
    count = download_many(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')


if __name__ == '__main__':
    main()
# END FLAGS_PY
