# -*- coding: utf-8 -*-

__author__ = 'Jim'

import hashlib


class SecretUtils:

    @staticmethod
    def md5(str):
        hash = hashlib.md5()
        hash.update(str.encode('utf-8'))
        return hash.hexdigest()


if __name__ == '__main__':
    md5_result = SecretUtils.md5("zhengwenfeng")
    print(md5_result)
