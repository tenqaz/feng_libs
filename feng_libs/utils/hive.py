# -*- coding: utf-8 -*-

"""该文件用来访问hive"""

__author__ = 'Jim'

from typing import Any, Optional, Iterable

from pyhive import hive

from txz_libs2.abc.sql import SQLStructure, SQLRow

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 10000
DEFAULT_DATABASE = "default"


class HiveClient(SQLStructure):
    """
    访问hive的client
    """

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                 username: Optional[str] = None, password: Optional[str] = None,
                 database: str = DEFAULT_DATABASE, **kwargs: Any):
        """

        :param host:
        :param port:
        :param username:
        :param password:
        :param database:
        :param kwargs:
        """

        self.conn: hive.Connection = None
        self.cursor: hive.Connection.cursor = None

        self.conn_property = {
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "database": database,
            **kwargs
        }

        self.open()

    def open(self) -> bool:
        """ 创建数据库连接 """

        try:
            self.conn = hive.Connection(**self.conn_property)
            self.cursor = self.conn.cursor()
        except Exception:
            return False
        else:
            return True

    def close(self) -> None:
        """ 关闭数据库连接 """
        if self.conn:
            self.conn.close()

        self.conn = None

    def select(self,
               database: str
               ) -> None:
        """ 选择数据库方法 """
        raise NotImplementedError("hive没有该方法")

    def query(self, sql: str, *args: Any) -> Iterable[SQLRow]:
        """ 查询方法 """
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            yield SQLRow(*row)

    def get(self,
            sql: str,
            *args: Any
            ) -> Optional[SQLRow]:
        """ 获取单条数据 """
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return SQLRow(*result)

    def execute(self,
                sql: str,
                *args: Any
                ) -> Any:
        """ 执行操作 """
        result = self.cursor.execute(sql)
        return result

    # cancel无法停止
    # def async_quert(self, sql: str, *args: Any) -> Iterable[SQLRow]:
    #     self.cursor.execute(sql, async_=True)
    #
    #     status = self.cursor.poll().operationState
    #     while status in (
    #             TOperationState.INITIALIZED_STATE,
    #             TOperationState.RUNNING_STATE):
    #         logs = self.cursor.fetch_logs()
    #         for message in logs:
    #             print(message)
    #         status = self.cursor.poll().operationState
    #
    #     result = self.cursor.fetchall()
    #     return result
    #
    # def async_cancel(self):
    #     self.cursor.cancel()
