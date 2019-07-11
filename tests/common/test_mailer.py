# -*- coding: utf-8 -*-

__author__ = 'Jim'

import pytest
from feng_libs.const.mailer import QQ_32_MAIL
from feng_libs.common.mailer import Mailer, send_from_me


@pytest.mark.skip(reason="example")
def test_example():
    Mailer.send("CrazyBoy", ('tenqaz@163.com', 'jim@txzing.com'), QQ_32_MAIL['server'], QQ_32_MAIL['server_host'],
                QQ_32_MAIL['user'], QQ_32_MAIL['password'], subject="这是一封邮件",
                notify_emails=('zhengwenfeng37@vip.qq.com',),
                content="this", attach_files=('F://work//tmp//tests//components//test_logger.py',
                                              "F://work//tmp//tests//workflow//test_download_data_action.py"))


@pytest.mark.skip(reason="example")
def test_send_from_me_example():
    send_from_me(('tenqaz@163.com', 'jim@txzing.com'), ('zhengwenfeng37@vip.qq.com',), "这是标题", "这是内容",
                 attach_files=('F://work//tmp//tests//components//test_logger.py',
                               "F://work//tmp//tests//workflow//test_download_data_action.py"))
