"""Download flags of top 20 countries by population

asyncio + httpx version

Sample run::

    $ python3 flags_asyncio_httpx.py
    CN EG BR IN ID RU NG VN JP DE TR PK FR ET MX PH US IR CD BD
    20 downloads in 0.35s

"""
# BEGIN FLAGS_ASYNCIO
import os
import time
import asyncio  # <1>

import httpx  # <2>


POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'http://flupy.org/data/flags'

DEST_DIR = 'downloaded/'


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


async def get_flag(client, cc):          # <3>
    cc = cc.lower()
    url = f'{BASE_URL}/{cc}/{cc}.gif'
    resp = await client.get(url)         # <4>
    return resp.read()                   # <5>


async def download_one(client, cc):      # <6>
    image = await get_flag(client, cc)   # <7>
    print(cc, end=' ', flush=True)
    save_flag(image, cc.lower() + '.gif')
    return cc


async def download_many(cc_list):
    async with httpx.AsyncClient() as client:                    # <8>
        tasks = [asyncio.create_task(download_one(client, cc))   # <9>
                 for cc in sorted(cc_list)]                      # <10>
        res = await asyncio.gather(*tasks)                       # <11>

    return len(res)


def main():  # <12>
    t0 = time.perf_counter()
    count = asyncio.run(download_many(POP20_CC))
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')


if __name__ == '__main__':
    main()
# END FLAGS_ASYNCIO
