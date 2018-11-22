"""
    主要用来获取数据的功能
"""
import telnetlib


def getUidListByAppid(appid, db):
    """
        通过appid 获取 uidList
    """
    db.select('txz_account')
    uid_df = db.read_dataframe_from_sql(
        "select uid from device_base where txz_app_id = '%s'" % appid,
        use_file=True
    )

    uid_list = uid_df["uid"].tolist()

    return uid_list


def get_license_uid_by_appid(appid, db):
    """
    获取appid 的已激活的 uid list
    """
    db.select("txz_account")

    uid_df = db.read_dataframe_from_sql(
        "select uid from license_base where txz_app_id = '%s'" % appid,
        use_file=True
    )

    uid_list = uid_df["uid"].tolist()
    return uid_list


def GetTimeAndAccessToken():
    """
        获取token
    """
    host = "m-bp1e17713aa9d764721.memcache.rds.aliyuncs.com"
    tn = telnetlib.Telnet(host=host, port=11211)
    tn.write(bytes("get wxc46e72f242ab5a19_access_token\n", encoding='utf-8'))
    finish = 'END'
    result = tn.read_until(bytes(finish, encoding='utf-8'))
    tn.close()
    result_list = str(result).split("\\r\\n")
    time_access_token = result_list[1].split(",")
    start_time = time_access_token[0]
    access_token = time_access_token[1]
    return start_time, access_token
