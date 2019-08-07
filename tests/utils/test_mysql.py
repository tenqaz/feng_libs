# -*- coding: utf-8 -*-

"""
@author: Jim
@project: feng_libs
@time: 2019/8/7 10:37
@desc:
"""

from __future__ import annotations

import pytest
from feng_libs.utils.mysql import MySQLConn


@pytest.mark.skip(reason="举个栗子")
def test_example():
    with MySQLConn(user="root", passwd="root1234") as db:
        db.select("datahub_poster")
        rst = db.query("select * from oozie_job_ooziejob")

        print(rst)
        assert 0


def test_dataframe_example():
    with MySQLConn(user="root", passwd="root1234") as db:
        db.select("datahub_poster")
        rst = db.query_dataframe("select * from oozie_job_ooziejob", ['id', 'task_id', 'delete'])

        print(rst)
        assert 0
