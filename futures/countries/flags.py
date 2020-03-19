"""Download flags of top 20 countries by population

Sequential version

Sample run::

    $ python3 flags.py
    BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN
    20 flags downloaded in 5.49s

"""
# BEGIN FLAGS_PY
import os
import time
import sys

import requests  # <1>

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()  # <2>

BASE_URL = 'http://flupy.org/data/flags'  # <3>

DEST_DIR = 'downloads/'  # <4>


def save_flag(img, filename):  # <5>
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):  # <6>
    cc = cc.lower()
    url = f'{BASE_URL}/{cc}/{cc}.gif'
    resp = requests.get(url)
    return resp.content


def download_many(cc_list):  # <7>
    for cc in sorted(cc_list):  # <8>
        image = get_flag(cc)
        print(cc, end=' ', flush=True)
        save_flag(image, cc.lower() + '.gif')

    return len(cc_list)


def main():  # <9>
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main()
# END FLAGS_PY
