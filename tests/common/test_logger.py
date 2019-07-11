# -*- coding: utf-8 -*-

__author__ = 'Jim'

import pytest

from txz_libs2.components.logger import Logger


@pytest.mark.skip
def test_example():
    # log = Logger(alarm_emails=['jim@txzing.com'], use_file=True)
    # log.debug("debug1")
    # log.error("error1")
    # log.debug("debug2")

    log = Logger()
    log.debug("sss")

    assert 0


def test_log(mocker):
    mocker_send = mocker.patch("txz_libs2.mailer.Mailer.send")
    mocker_stream_emit = mocker.patch("logging.StreamHandler.emit")
    mocker_file_emit = mocker.patch("logging.FileHandler.emit")

    log = Logger(use_file=True, alarm_emails=['jim@txzing.com'])

    log.debug("zhangsan")
    log.error("lisi")

    mocker_stream_emit.assert_called()
    mocker_file_emit.assert_called()
    mocker_send.assert_called_once()
