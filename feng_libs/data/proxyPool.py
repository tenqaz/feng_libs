import asyncio

import aiohttp


class ProxyPool:

    url = 'http://www.wenfengboy.com/proxy'

    def __init__(self):
        pass

    @staticmethod
    async def get_proxy():
        """获取http代理

        Return:
            返回一个http代理. str

        """

        async with aiohttp.ClientSession() as client:
            rsp = await client.get(ProxyPool.url, data={"method": "gain"})
            proxy = await rsp.text()
            proxy = f"http://{proxy}"

        return proxy


async def main():
    print(await ProxyPool.get_proxy())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
