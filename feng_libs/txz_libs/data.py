"""
    主要用来获取数据的功能
"""
import telnetlib
from collections import defaultdict


def get_license_info_by_uid_list(uid_list, db):
    """ 获取uid_list 的激活信息

    Args:
        uid_list
        db: 数据库

    Returns:
        rst: list. license_base表中的数据.

        数据结构: uid, txz_app_id, first_use_time, live_id, create_time
    """
    db.select("txz_account")
    uid_len = len(uid_list)

    sql = f"select * from license_base where uid in ({('%s,'*uid_len)[:-1]})"
    rst = db.query(sql, *uid_list)

    return rst


def get_license_uid_list_by_appid_list(appid_list, db):
    """ 获取 appid_list 的已激活的 uid list

    Args:
        appid_list:
        db:

    Returns:
        uid_list:

    """
    db.select("txz_account")
    appid_len = len(appid_list)
    rst = db.query(
        "select uid from license_base where txz_app_id = "
        f"({('%s,'*appid_len)[:-1]})",
        *appid_list
    )

    uid_list = [record['uid'] for record in rst]
    return uid_list


def get_shipment_info_by_appid_list(appid_list, db, startTime=None, endTime=None):
    """ 获取 appid_list 的出货量

    Args:
        appid_list:
        startTime: 可选, 从这个时间开始往后的激活量
        endTime: 可选, 到这个时间结束

    Return:
        rst: list. 表中数据

        部分数据结构: uid, txz_app_id, imei, create_time

    """

    db.select("txz_account")
    appid_len = len(appid_list)

    if startTime:
        if not endTime:
            endTime = Moment().format()

        sql = "select * from device_base where txz_app_id in " \
              f"({('%s,'*appid_len)[:-1]}) and create_time between " \
              f"'{startTime}' and date_add('{endTime}', interval 1 day)"
    else:
        sql = "select * from device_base where txz_app_id in " \
              f"({('%s,'*appid_len)[:-1]})"

    rst = db.query(sql, *appid_list)
    return rst


def get_shipment_uid_list_by_appid_list(appid_list, db):
    """ 通过appid_list 获取 uid_list

        Args:
            appid_list: appid的列表

        Returns:
            app_uidList_dict: appid对应的uidlist.
    """

    app_uidList_dict = defaultdict(list)

    appid_len = len(appid_list)

    db.select('txz_account')
    sql = "select txz_app_id, uid from device_base where " \
          f"txz_app_id in ({('%s,'*appid_len)[:-1]})"
    rst = db.query(sql, *appid_list)
    for record in rst:
        app_uidList_dict[record['txz_app_id']].append(record['uid'])

    return app_uidList_dict


def get_shipment_count_by_appid_list(appid_list, db, end_time=None):
    """ 获取 appid list 的出货量.

    两种办法：
        1. 查询 deviceBase 表
        2. 查询 user_static_data 静态文件
        查询的也挺快的，就用第一种。第二种比较耗时，而且不是最新的。


        Args:
            appid_ist:
            db:
            end_time: 截止时间. 2018-12-01 00:00:00

        Returns:
            各个appid的出货量. map[appid] = count

    """
    appid_count = dict()

    app_len = len(appid_list)

    db.select("txz_account")

    if end_time:
        sql = "select txz_app_id,count(1) as app_count from device_base " \
            f"where txz_app_id in ({('%s,'*app_len)[:-1]}) and "  \
            f"create_time < '{end_time}' group by txz_app_id"
    else:
        sql = "select txz_app_id,count(1) as app_count from device_base " \
            f"where txz_app_id in ({('%s,'*app_len)[:-1]}) group by txz_app_id"

    rst = db.query(sql, *appid_list)
    for record in rst:
        appid_count[record['txz_app_id']] = record['app_count']
    return appid_count


def get_shipment_appidList_by_uidList(uid_list, db):
    """ 通过uid 获取 appid和uid对应关系的字典。

        通过查询device_base表查询得到结果

        Args:
            uid_list:
            db:

        Returns:
            app_uidList_dict: appid对应的uidlist.

    """
    app_uidList_dict = defaultdict(list)

    # 将uid int 转 str
    uid_list = [str(uid) for uid in uid_list]

    db.select("txz_account")
    sql = "select txz_app_id, uid from device_base where uid in " \
          f"({','.join(uid_list)})"
    rst = db.query(sql)
    for record in rst:
        app_uidList_dict[record['txz_app_id']].append(record['uid'])
    return app_uidList_dict


def get_shipment_uid_list_by_imei_list(imei_list, db):
    """ 通过imei获取uid

    Args:
        imei_list: imei的列表

    Return:
        返回 imei 对应的 uid. dict

    """
    uid_imei_map = {}
    db.select("txz_account")
    sql = "select uid, imei from device_base where imei in ({})".format(
        ",".join(imei_list))
    rst = db.query(sql)
    for record in rst:
        uid_imei_map[record['imei']] = record['uid']

    return uid_imei_map


def get_last_login_time_by_uid_list(uid_list, db):
    """ 获取uid最后登录的时间.

    Args:
        uid_list:
        db:

    Returns:
        uid_lasttime_dict: dict, 各个uid对应的最后登录时间

    """
    uid_lasttime_dict = dict()

    db.select("txz_account")
    uid_len = len(uid_list)
    sql = f"select uid, time_last_login from user_base_00 where uid in ({('%s,'*uid_len)[:-1]})"
    rst = db.query(sql, *uid_list)

    for record in rst:
        uid_lasttime_dict[record['uid']] = record['time_last_login']

    return uid_lasttime_dict


def get_uid_by_diary(filename, attr_list, start_time, end_time):
    """ 通过le文件获得 无重复的 uid

        Args:
            filename: 文件名
            attr_list: 属性名 列表
            start_time: 开始时间， 需要精确到时分秒  eq:2018-01-01 00:00:00
            end_time: 结束时间

        Return:
            每个属性的uid_set的defaultmap
    """

    start_time = Moment(start_time).timestamp()
    end_time = Moment(end_time).timestamp()

    attr_uidSet = defaultdict(set)

    for it in async_read_diary_serialize(filename, ErrorInfo):

        if (it[1] in attr_list and (
            it[3] >= start_time and it[3] <= end_time
        )):
            attr_uidSet[it[1]].add(it[0])

    return attr_uidSet


def read_diary(time_attr_list_tuple):
    """ 读取一天的流水文件, 获取指定属性的非重复的 uid_Set

        Todo: 目前精确到天，以后如果有需要就精确到秒

        Args:
            time_attr_list_tuple:
                [0]: time
                [1]: attr_list

        Returns:
            attr_uidSet
            每个属性的 uid 集合
    """
    _time = time_attr_list[0]
    print(_time)
    attr_list = time_attr_list[1]

    path = '/txz_user_action_data/txz/logicError'

    attr_uidSet_all = defaultdict(set)

    file_list = glob(f"{path}/{_time}.*le")
    if len(file_list) == 0:
        os.system(f"7za x {path}/{_time}.7z -o{path}")
        file_list = glob(f"{path}/{_time}.*.le")

    for _file in file_list:
        attr_uidSet = get_uid_by_diary(
            _file, attr_list, _time+" 00:00:00", _time+" 23:59:59")

        for key, value in attr_uidSet.items():
            attr_uidSet_all[key] = attr_uidSet[key] | attr_uidSet_all[key]

    return attr_uidSet_all


def get_daily_active_by_appid_list(appid_list, _time, db):
    """ 获取 appid 某天的 日活

        Args:
            appid_list: appid的列表
            _time: 哪一日的日活
            db: 数据库

        Returns:
            daily_active_dict: appid对应的日活

    """
    daily_active_dict = {}

    db.select("txz_stats")
    appid_len = len(appid_list)
    sql = f"select txz_app_id, count from active_daily where txz_app_id in ({('%s,'*appid_len)[:-1]}) and to_days(last_time) = to_days(%s)"
    rst = db.query(sql, *appid_list, _time)
    for record in rst:
        daily_active_dict[record['txz_app_id']] = record['count']

    return daily_active_dict


def get_monthly_active_by_appid(appid_list, _time, db):
    """ 获取 appid 某天的 月活

        Args:
            appid_list: appid的列表
            _time: 哪一月的月活
            db: 数据库

        Returns:
            month_active_dict: appid对应的月活

    """
    month_active_dict = {}

    db.select("txz_stats")
    appid_len = len(appid_list)
    sql = f"select txz_app_id, count from active_monthly where txz_app_id in ({('%s,'*appid_len)[:-1]}) and month(last_time) = month(%s)"
    rst = db.query(sql, *appid_list, _time)
    for record in rst:
        month_active_dict[record['txz_app_id']] = record['count']

    return month_active_dict


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
