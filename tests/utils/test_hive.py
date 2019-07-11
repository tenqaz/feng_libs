# -*- coding: utf-8 -*-

__author__ = 'Jim'

import pytest

from txz_libs2.hive import HiveClient, DEFAULT_PORT, DEFAULT_DATABASE

property = {
    "host": "txz-data0"
}

query_sql = "select count(*) from test"


@pytest.fixture()
def mock_hive_conn_open(mocker):
    return mocker.patch("txz_libs2.hive.HiveClient.open")


@pytest.fixture()
def mock_hive_conn(mocker):
    return mocker.patch("pyhive.hive.Connection")


@pytest.mark.skip(reason="这是一个demo")
def test_example():
    with HiveClient(**property) as client:
        sql = "select * from base_crash where date = '2019-05-02' limit 2"
        result = client.query(sql)
        print(result)
        for record in result:
            print(record.keys())
            print(len(record))

        # result = client.get(sql)
        # print(result)

    assert 0


def test_hive_initialize(mock_hive_conn_open):
    with HiveClient(**property) as client:
        assert client.conn_property == dict(
            host="txz-data0",
            port=DEFAULT_PORT,
            username=None,
            password=None,
            database=DEFAULT_DATABASE
        )


# def test_select(mock_hive_conn):
#     with HiveClient(**property) as client:
#         client.select("test_db")
#
#         mock_hive_conn.return_value.select().assert_called_once_with("test_db")

def test_query(mock_hive_conn):
    mock_cursor = mock_hive_conn.return_value.cursor
    mock_cursor.return_value.fetchall.return_value = None

    with HiveClient(**property) as client:
        with pytest.raises(TypeError):
            next(client.query(query_sql))

        mock_cursor.return_value.fetchall.assert_called_once()
        mock_cursor.return_value.execute.assert_called_once_with(query_sql)


def test_execute(mock_hive_conn):
    mock_cursor = mock_hive_conn.return_value.cursor
    mock_cursor.return_value.fetchone.return_value = None

    with HiveClient(**property) as client:
        client.execute(query_sql)

        mock_cursor.return_value.execute.assert_called_once_with(query_sql)


def test_get(mock_hive_conn):
    mock_cursor = mock_hive_conn.return_value.cursor
    mock_cursor.return_value.fetchone.return_value = None

    with HiveClient(**property) as client:
        with pytest.raises(TypeError):
            client.get(query_sql)

        mock_cursor.return_value.execute.assert_called_once_with(query_sql)
        mock_cursor.return_value.fetchone.assert_called_once()
