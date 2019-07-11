# -*- coding: utf-8 -*-

__author__ = 'Jim'

import pytest

from txz_libs2.async_mysql import AsyncMysql
import asynctest
from unittest.mock import MagicMock
import asyncio
from aiohttp.test_utils import make_mocked_coro
import aiomysql


@pytest.mark.skip
@pytest.mark.asyncio
async def test_example():
    async with AsyncMysql(host="192.168.3.140", password="root1234") as client:
        await client.select("test")
        # result = await client.query("select * from test1")
        result = await client.get("select * from test1")
        print(result)

    assert 0


async def return_async_value(val):
    return val


async def mock_close(self, val):
    return val


@pytest.fixture()
async def mock_connect(mocker):
    mocker_connect = mocker.patch("aiomysql.connect")
    mocker_cursor = mocker_connect.return_value.cursor
    mocker_connect.return_value = return_async_value(mocker_cursor)
    mocker_cursor.cursor = return_async_value

    return mocker_connect


@pytest.mark.asyncio
async def test_init(mock_connect):
    property = {
        "user": "root",
        "password": "root1234",
        "host": "192.168.0.1"
    }



    async with AsyncMysql(**property) as client:
        await client.select("test")

        # result = await client.get("select * from test1")

        # assert client.user == "root"
        pass
