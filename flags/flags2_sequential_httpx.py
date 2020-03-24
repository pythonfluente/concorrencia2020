"""Download flags of countries (with error handling).

Sequential version using the HTTPx library

Sample run::

    $ python3 flags2_sequential_httpx.py -s DELAY b
    DELAY site: http://localhost:8002/flags
    Searching for 26 flags: from BA to BZ
    1 concurrent connection will be used.
    --------------------
    17 flags downloaded.
    9 not found.
    Elapsed time: 13.36s

"""

import collections

import httpx
import tqdm

from flags2_common import main, save_flag, HTTPStatus, Result


DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

# BEGIN FLAGS2_BASIC_HTTP_FUNCTIONS
def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = httpx.get(url)
    if resp.status_code != 200:  # <1>
        resp.raise_for_status()
    return resp.content


def download_one(cc, base_url, verbose=False):
    try:
        image = get_flag(base_url, cc)
    except httpx._exceptions.HTTPError as exc:  # <2>
        resp = exc.response
        if resp is not None and resp.status_code == 404:
            status = HTTPStatus.not_found  # <3>
            msg = 'not found'
        else:  # <4>
            raise
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose:  # <5>
        print(cc, msg)

    return Result(status, cc)  # <6>
# END FLAGS2_BASIC_HTTP_FUNCTIONS

# BEGIN FLAGS2_DOWNLOAD_MANY_SEQUENTIAL
def download_many(cc_list, base_url, verbose, max_req):
    counter = collections.Counter()  # <1>
    cc_iter = sorted(cc_list)  # <2>
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)  # <3>
    for cc in cc_iter:  # <4>
        try:
            result = download_one(cc, base_url, verbose)  # <5>
        except httpx._exceptions.HTTPError as exc:  # <6>
            error_msg = f'HTTP error {exc}'
        else:  # <8>
            error_msg = ''
            status = result.status

        if error_msg:
            status = HTTPStatus.error  # <9>
        counter[status] += 1  # <10>
        if verbose and error_msg: # <11>
            print('*** Error for {}: {}'.format(cc, error_msg))

    return counter  # <12>
# END FLAGS2_DOWNLOAD_MANY_SEQUENTIAL

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
