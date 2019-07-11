"""
    author: jim
    date: 2019-01-17

    对mysql数据库的同步和异步操作.

    TODO: 未支持事务
    TODO: 未支持连接池

    遇到的奇葩问题.
    cursor 的占位符不支持 %d 整型也用%s

"""
import asyncio
from typing import Type, Optional, Tuple

import aiomysql


class AsyncMysql():
    DICT_CURSOR = aiomysql.DictCursor
    SS_CURSOR = aiomysql.SSCursor
    SS_DICT_CURSOR = aiomysql.SSDictCursor

    def __init__(
            self, host: str = "127.0.0.1",
            port: int = 3306,
            user: str = "root",
            password: Optional[str] = None,
            loop: Optional[Type[asyncio.AbstractEventLoop]] = None,
            db: str = None,
            cursor_class: Type[aiomysql.Cursor] = DICT_CURSOR
    ):
        """
        初始化

        :param host: mysql地址
        :param port: mysql端口
        :param user: 用户名
        :param password: 密码
        :param loop: 事件循环.
        :param db: 数据库
        :param cursor_class: 使用的游标类。
            DICT_CURSOR，返回的字典数据. 
            SS_CURSOR，使用在数据量大，网络慢, 内存不足场景。是无缓存形式。
            SS_DICT_CURSOR, 无缓存的字典数据。
        """

        self.cursor: aiomysql.Cursor = None
        self.conn: aiomysql.Connection = None

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.loop = loop or asyncio.get_running_loop()
        self.db = db
        self.cursor_class = cursor_class

    async def connect(self):
        """
        数据库连接
        """
        self.conn = await aiomysql.connect(
            host=self.host, port=self.port, user=self.user,
            password=self.password, db=self.db, loop=self.loop
        )

        self.cursor = await self.conn.cursor(self.cursor_class)

    async def select(self, db: str):
        """
            选择使用数据库

            :param db: 数据库名
        """

        await self.conn.select_db(db)

    async def query(self, sql: str, num: int = None,
                    args: Optional[Tuple] = None):
        """
        查询数据库.
        占位符不支持%d, 整型也是用%s

            :param: sql: 查询语句
            :param: num: 查询返回的数量
            :param: args: 占位符的参数
        """
        await self.cursor.execute(sql, args=args)

        if num:
            result = await self.cursor.fetchmany(num)
        else:
            result = await self.cursor.fetchmany()

        return result

    async def get(self, sql: str, args=None):
        """
        获取一行数据
        :param sql:
        :param args: Tuple: 占位符参数
        :return:
        """
        await self.cursor.execute(sql, args=args)
        return await self.cursor.fetchone()

    async def execute(self, sql: str, args: Optional[Tuple] = None,
                      many: bool = False):
        """
            insert, delete, update 执行

            :param: sql: 增删改语句
            :param: args: 占位符参数
            :param: many: 是否支持执行多个数据. list(tuple, tuple...)
        """

        if many:
            ret = await self.cursor.executemany(sql, args=args)
        else:
            ret = await self.cursor.execute(sql, args=args)
        await self.conn.commit()
        return ret

    async def close(self):
        if self.conn:
            self.conn.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


async def create_async_mysql_client(
        host: str = "127.0.0.1", port: int = 3306, user: str = "root",
        password: str = "55555",
        loop: Optional[Type[asyncio.AbstractEventLoop]] = None,
        db: str = None,
        cursor_class: Type[aiomysql.Cursor] = AsyncMysql.DICT_CURSOR,
):
    """
    获取异步的MysqlClient对象

        参数看 __init__
    """

    mysqlClient = AsyncMysql(host, port, user, password, loop, db,
                             cursor_class)
    await mysqlClient.connect()
    return mysqlClient


async def main():
    # client = await create_async_mysql_client(password="root1234")
    # await client.select("test")
    # result = await client.get("select * from test1")
    # print(result)
    # await client.close()

    async with AsyncMysql(password="root1234") as client:
        await client.select("test")
        # result = await client.query("select * from test1")
        result = await client.get("select * from test1")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
