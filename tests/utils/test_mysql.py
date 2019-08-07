# -*- coding: utf-8 -*-

"""
@author: Jim
@project: feng_libs
@time: 2019/8/7 10:37
@desc:
"""

from __future__ import annotations

import pytest
from feng_libs.utils.mysql import MySQLConn, get_sqlalchemy_engine
import pandas as pd


@pytest.mark.skip(reason="举个栗子")
def test_example():
    with MySQLConn(user="root", passwd="root1234") as db:
        db.select("datahub_poster")
        rst = db.query("select * from oozie_job_ooziejob")

        print(rst)
        assert 0


@pytest.mark.skip(reason="再给你个栗子")
def test_sqlalchemy_example():
    engine = get_sqlalchemy_engine(user="root", passwd="root1234", database='datahub_poster')
    df = pd.read_sql("select * from oozie_job_ooziejob", engine)
    print(df)
    assert 0
