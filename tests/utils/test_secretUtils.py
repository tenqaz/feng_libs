# -*- coding: utf-8 -*-

__author__ = 'Jim'

from feng_libs.utils.secret_utils import SecretUtils


def test_md5():
    md5_result = SecretUtils.md5("zhengwenfeng")
    assert md5_result == "2e91bc6bd41dba94f16141b8c37f0854"
