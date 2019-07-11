# -*- coding: utf-8 -*-

"""
日志工具
"""

__author__ = 'Jim'

import logging
import os
import sys
from typing import Optional, List, Dict, Any
from feng_libs.common.mailer import send_from_me

# 默认的日志等级
DEFAULT_LEVEL_BASE = logging.DEBUG
DEFAULT_LEVEL_FILE = logging.DEBUG
DEFAULT_LEVEL_CONSOLE = logging.DEBUG
DEFAULT_LEVEL_EMAIL = logging.ERROR


class EmailAlarmHandle(logging.Handler):
    """
    邮件告警
    """

    def __init__(self, alarm_emails: List[str]):
        self.alarm_emails = alarm_emails
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        subject = f"{record.pathname} 报错"
        send_from_me(self.alarm_emails, subject=subject, content=msg)


class Logger:
    """
        日志工具
    """

    def __init__(self,
                 name: str = os.path.split(os.path.splitext(sys.argv[0])[0])[
                     -1],
                 log_level: Optional[Dict[str, int]] = None,
                 alarm_emails: Optional[List[str]] = None,
                 use_file: bool = False,
                 log_file: str = f"{os.path.splitext(sys.argv[0])[0]}.log",
                 use_console: bool = True
                 ):
        """
        三种日志输出方式: （默认使用控制台）
            控制台: 所有的日志，默认输出到stderr中。 默认级别: DEBUG
            日志文件: 所有的日志。默认级别: DEBUG
            邮件: 只有ERROR级别以上的的日志。 默认级别: ERROR

        :param name: log名称。默认是文件名。

        :param log_level: log级别。dict
            分别对应的是文件、控制台和邮件的日志等级
            { file: file_level, console: console_level, email: email_level }

        :param alarm_emails: 告警的email列表。
        :param use_file: 是否将日志保存到文件中。
        :param log_file: 文件路径文件名。默认在调用的文件目录下创建。
                创建的日志文件名是调用的文件名.log。只有当use_file为True才会被使用

        :param use_console: 是否打印到控制台。
        """

        log_level = log_level if log_level else dict(
            file=DEFAULT_LEVEL_FILE,
            email=DEFAULT_LEVEL_EMAIL,
            console=DEFAULT_LEVEL_CONSOLE
        )

        # 获取log的name
        self.logger = logging.getLogger(name)

        # 这个是整体级别，handle都是基于此级别再去分级别
        self.logger.setLevel(DEFAULT_LEVEL_BASE)

        # format
        formatter = logging.Formatter(
            fmt="%(levelname)s %(asctime)s %(name)s %(filename)s %(funcName)s "
                "%(lineno)d: %(message)s",
            datefmt="%Y-%m-%d  %H:%M:%S"
        )

        # handler
        if use_file:  # 日志文件
            file_handle = logging.FileHandler(log_file, encoding="utf-8")
            file_handle.setFormatter(formatter)
            file_handle.setLevel(log_level.get('file', DEFAULT_LEVEL_FILE))
            self.logger.addHandler(file_handle)

        if alarm_emails:
            email_handle = EmailAlarmHandle(alarm_emails)
            email_handle.setLevel(log_level.get('email', DEFAULT_LEVEL_EMAIL))
            email_handle.setFormatter(formatter)
            self.logger.addHandler(email_handle)

        if use_console:
            stream_handle = logging.StreamHandler()
            stream_handle.setFormatter(formatter)
            stream_handle.setLevel(
                log_level.get('console', DEFAULT_LEVEL_CONSOLE))
            self.logger.addHandler(stream_handle)

    def __getattr__(self, item: Any) -> Any:
        return getattr(self.logger, item)
