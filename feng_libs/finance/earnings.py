#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File: earnings.py
@Time: 2024/11/26 12:59:56
@Author: Jim
@Contact: zhengwenfeng37@gmail.com
@Desc: 
    收益计算
'''


class Earnings:

    @staticmethod
    def annual_rate_of_return(total_yield: float, year: int) -> float:
        """ 计算年化收益率
            Args:
                total_yield: 总收益率
                year: 年数

            计算公式：(总收益率+1)开年数的次方再减1

            example:
                总收益率为1250%,所以total_yield=12.5,持有17年,year=17,其结果为0.165,也就是年化有16.5%
                计算：(12.5+1)开17次方再减1 结果为: 0.165
        """

        res = (total_yield + 1) ** (1 / year) - 1
        print(res)
