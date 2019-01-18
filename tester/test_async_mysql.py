"""
    author: jim
    date: 2019--01-18

    用于测试异步数据库操作的测试.
"""

import random
import pymysql
import timeit
import asyncio
# import feng_libs.utils import mysqlClient
import feng_libs.utils.mysqlClient


def sync():
    """
        426.5523661 秒
    """
    name_list = ["zhangsan", "lisi", "wangwu", "zhaoliu"]

    db = pymysql.connect("localhost", "root", "55555")
    db.select_db("test")
    cursor = db.cursor()

    for j in range(1, 10):

        for i in range(10000):
            name_int = random.randint(0, 3)

            sql = f"insert into test{j}(name) values('{name_list[name_int]}')"
            cursor.execute(sql)
            db.commit()
    db.close()


async def insert_data(table_index):
    pass


async def a_sync():
    db = await mysqlClient.create_mysql_client()


def async_test():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(a_sync())


if __name__ == "__main__":
    # _time = timeit.timeit(sync, number=1)

    async_test()
