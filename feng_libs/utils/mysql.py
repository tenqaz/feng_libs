# -*- coding: utf-8 -*-

"""
@author: Jim
@project: feng_libs
@time: 2019/8/7 9:59
@desc: mysql数据库连接
"""

from __future__ import annotations

import functools
import time
from types import TracebackType
from typing import Optional, Any, cast, Callable, TypeVar, Type, List

from pymysql import Connection
from pymysql.cursors import Cursor, SSCursor, DictCursor, SSDictCursor
import pandas as pd

T = TypeVar('T')

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 3306

MYSQL_CURSOR = {
    "default": Cursor,
    "SSCursor": SSCursor,
    # 使用SSCursor代替普通游标。这个cursor不会将数据复制到内存中，它从数据库存储块中读取记录，然后一条条返回。这样做的好处是客户端使用的内存少很多，并且当通过一个慢速网络或结果集非常大时，返回的行要快得多。
    "DictCursor": DictCursor,  # 返回字典数据
    "SSDictCursor": SSDictCursor,
}


def operation_wraps(func: Callable[..., T]) -> Callable[..., T]:
    """ 检查数据库连接操作 """

    @functools.wraps(func)
    def wrapper(self: MySQLConn, *args: Any) -> T:
        if not all([self.conn, self.cursor]):
            raise Exception("MySQLConn disconnect ! Please check configure. ")

        offline = True
        retry_count = 0
        while offline and retry_count < 10:
            try:
                cast(Connection, self.conn).ping()  # ping 一下确认连接生效
                offline = False
            except Exception:
                if self.open():  # 尝试重新创建连接
                    offline = False
                    break
                retry_count += 1
                time.sleep(0.1 * retry_count)  # 休眠

        if not offline:
            return func(self, *args)
        raise Exception("MySQLConn disconnect ! Please check configure. ")

    return wrapper


class MySQLConn():
    """ mysql 连接 """

    def __init__(self,
                 host: str = DEFAULT_HOST,
                 port: int = DEFAULT_PORT,
                 user: Optional[str] = None,
                 passwd: Optional[str] = None,
                 database: Optional[str] = None,
                 cursorclass: Cursor = MYSQL_CURSOR["default"],
                 charset: str = "utf8",
                 connect_timeout: int = 10,
                 **kwargs: Any
                 ) -> None:
        """ initialize mysql connection

        :param host:
        :param port:
        :param user:
        :param passwd:
        :param database: 数据库名
        :param cursorclass: See `pymysql.connect` `cursorclass` argument. It
                            includes Cursor, DictCursor, DictCursorMixin, SSCursor, SSDictCursor
        :param charset: Charset you want to use.
        :param connect_timeout: Timeout before throwing an exception when connecting.
                                (default: 10, min: 1, max: 31536000)
        :param kwargs: See `pymysql.Connection` for more information
        """
        self.conn: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None

        self.conn_properties = dict(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=database,
            cursorclass=cursorclass,
            charset=charset,
            connect_timeout=connect_timeout,
            **kwargs
        )

        self.open()

    def open(self) -> bool:
        """ 打开连接 """
        try:
            self.conn = Connection(**self.conn_properties)
            self.cursor = self.conn.cursor()
        except Exception:
            return False
        else:
            return True

    def close(self) -> None:
        """ 关闭连接 """
        if self.conn:
            cast(Connection, self.conn).close()
        self.conn = None

    def select(self,
               database: str
               ) -> None:
        cast(Connection, self.conn).select_db(database)  # type: ignore
        self.conn_properties["database"] = database

    @operation_wraps
    def query(self,
              sql: str,
              *args: Any
              ) -> Any:
        """ 查询多条数据 """
        cast(Cursor, self.cursor).execute(sql, *args)
        result = cast(Cursor, self.cursor).fetchall()
        if result is None:
            return

        return result

    @operation_wraps
    def query_dataframe(self, sql: str, column: List):
        """

        :param column:
        :return:
        """

        rst = self.query(sql)
        return pd.DataFrame(rst, columns=column)




    @operation_wraps
    def get(self,
            sql: str,
            *args: Any
            ) -> Any:
        """ 获取一条数据 """
        cast(Cursor, self.cursor).execute(sql, *args)
        row = cast(Cursor, self.cursor).fetchone()

        return row

    @operation_wraps
    def execute(self,
                sql: str,
                *args: Any
                ) -> int:
        """ 执行 execute 语句，返回影响行数

        :param sql:
        :param args:
        :return:
        """
        return cast(Cursor, self.cursor).execute(sql, *args)

    def last_row_id(self) -> Optional[int]:
        """ Return the id of the last affected rows """
        return cast(Cursor, self.cursor).lastrowid

    def commit(self) -> None:
        """ 提交修改 """
        if self.conn is None:
            return
        cast(Connection, self.conn).commit()

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]
                 ) -> None:
        """
        上下文退出管理器
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.commit()
        self.close()

    def __enter__(self) -> None:
        """
        上下文进入管理器
        :return:
        """
        return self