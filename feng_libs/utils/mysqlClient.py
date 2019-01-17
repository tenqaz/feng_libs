"""
    author: jim
    date: 2019-01-17

    对mysql数据库的同步和异步操作.

    遇到的奇葩问题.
    cursor 的占位符不支持 %d 整型也用%s

"""
import aiomysql
import pymysql
from tornado.ioloop import IOLoop
import asyncio


class MysqlClient():

    def __init__(
            self, host="127.0.0.1", port=3306, user="root", password="55555",
            loop=None, db=None, en_pool=False):
        """
        初始化

        :param host: mysql地址
        :param port: mysql端口
        :param user: 用户名
        :param password: 密码
        :param loop: 事件循环
        :param db: 数据库
        :param en_pool: 是否使用连接池
        """
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._loop = loop or asyncio.get_event_loop()
        self._db = db
        self._en_pool = en_pool

    @property
    def user(self):
        """
            当前的用户
        """
        return self._user

    @property
    def host(self):
        """
            当前连接地址
        """
        return self._host

    @property
    def db(self):
        """
            当前使用的数据库
        """
        return self._db

    @property
    def port(self):
        """
            当前端口号
        """
        return self._port

    async def _connect(self):

        self._conn = await aiomysql.connect(
            host=self._host, port=self._port, user=self._user,
            password=self._password, db=self._db, loop=self._loop
        )

        self._cursor = await self._conn.cursor()

    async def _connect_pool(self):
        pass

    async def select(self, db):
        """
            选择使用数据库

            :param db: 数据库名
        """

        await self._conn.select_db(db)

    async def async_query(self, sql, num=None, args=None):
        """
        查询数据库.
        占位符不支持%d, 整型也是用%s

            :param: sql: 查询语句
            :param: num: 查询返回的数量
            :args: 占位符的参数
        """
        await self._cursor.execute(sql, args=args)

        if num:
            result = await self._cursor.fetchmany(num)
        else:
            result = await self._cursor.fetchall()

        return result


async def create_client(
    host="127.0.0.1", port=3306, user="root", password="55555", loop=None,
    db=None, en_pool=False
):
    """
    获取异步的MysqlClient对象

        参数看 __init__
    """

    mysqlClient = MysqlClient(host, port, user, password, loop, db, en_pool)
    await mysqlClient._connect()

    return mysqlClient


async def main():
    mysqlClient = await create_client()
    await mysqlClient.select("test")
    sql = "select * from student where id = %s"
    result = await mysqlClient.async_query(sql, args=[1,])
    print(result)


if __name__ == "__main__":
    IOLoop.current().run_sync(main)
