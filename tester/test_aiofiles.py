"""
    用于测试 aiofiles 异步效率。

    虽然确实快于同步，但是快不了多少。
"""

import aiofiles
import asyncio
import timeit

i = 0


def sync_io():
    """
        43.0476731
    """
    global i

    with open("0.txt", "r", encoding="gbk", errors='ignore') as f:
        text = f.read()

    with open(f"./data/{i}.txt", "w", encoding="gbk", errors='ignore') as f:
        f.write(text)

    i += 1


async def work(i):
    async with aiofiles.open("0.txt", "r", encoding="gbk", errors='ignore') as f:
        text = await f.read()

    async with aiofiles.open(f"./data/{i}.txt", "w", encoding="gbk", errors='ignore') as f:
        await f.write(text)


def async_io():
    """
        40.1616362
    """

    loop = asyncio.get_event_loop()

    work_list = [work(i) for i in range(200)]

    loop.run_until_complete(asyncio.gather(*work_list))


if __name__ == "__main__":

    _time = timeit.timeit(sync_io, number=200)

    # _time = timeit.timeit(async_io, number=1)
    print(_time)
