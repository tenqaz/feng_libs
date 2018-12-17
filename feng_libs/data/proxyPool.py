"""
    代理池。

    请求代理池获取代理。代理池服务器是wenfengboy。
"""
import asyncio

import aiohttp

from feng_libs.const.server import WENFENG_BOY


class ProxyPool:

    url = f'http://{WENFENG_BOY["host"]}/proxy'

    def __init__(self):
        pass

    @staticmethod
    async def get_proxy():
        """获取http代理

        Return:
            返回一个http代理. str

        """

        gain_url = f"{ProxyPool.url}/gain"

        async with aiohttp.ClientSession() as client:
            rsp = await client.get(gain_url)
            proxy = await rsp.text()
            proxy = f"http://{proxy}"

        return proxy


async def main():
    print(await ProxyPool.get_proxy())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
