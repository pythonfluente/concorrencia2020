#!/usr/bin/env python3

# Inspired by
# https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/

import asyncio
import time


async def countdown(label, start_time, delay):
    tabs = (ord(label) - ord('A')) * '\t'
    n = 3
    while n > 0:
        await asyncio.sleep(delay)
        #time.sleep(delay)
        dt = time.perf_counter() - start_time
        print('━' * 50)
        print(f'{dt:7.2f}s \t{tabs}{label}: {n}')
        n -= 1


async def main():
    t0 = time.perf_counter()
    tasks = [
        asyncio.create_task(countdown('A', t0, .7)),
        asyncio.create_task(countdown('B', t0, 2)),
        asyncio.create_task(countdown('C', t0, .3)),
        asyncio.create_task(countdown('D', t0, 1)),
    ]
    await asyncio.wait(tasks)
    print('━' * 50)

if __name__ == '__main__':
    asyncio.run(main())
