"""
    author: jim
    date: 2018-11-19

    同行者关于场景的过滤。

"""

import json
import time
from collections import Counter

from txz_libs.proto.py.report_manager_pb2 import UAT_VOICE, UAT_VOICE_REPEAT

scene_list = {
    'unknow': 'scene_unknow', '唤醒': 'scene_wakeup',
    '设置唤醒词': 'scene_set_wakeup_keywords', '执行命令': 'scene_command',
    'app': 'scene_app', '打电话': 'scene_call', '导航相关': 'scene_nav',
    'poi': 'scene_poi', '音乐相关': 'scene_music', '天气相关': 'scene_weather',
    '股票相关': 'scene_stock', '相关位置': 'scene_location',
    '交通相关': 'scene_traffic', '限行相关': 'scene_limit',
    '不支持操作': 'scene_unsupport', '没有说话': 'scene_empty',
    '微信相关': 'scene_wechat', '查询相关': 'scene_query',
    '系统相关': 'scene_system', '上次会话更改': 'scene_fix',
    'core_相关': 'scene_txz', '电台相关': 'scene_radio',
    '闲聊相关': 'scene_chat'
}


# ------------- music ------------------------------

def scene_music(df):
    """音乐相关"""
    return df[df.json.str.contains('"scene":"music"') |
              df.json.str.contains('"scene":"audio"') |
              df.json.str.contains('"r":"msc"')]


def song_df(df):
    """
    获取各种歌曲次数的字典
    """
    df_music = df[df.json.str.contains('"scene":"music"')]
    music_dict = df_music.json.str.extract(
        r'"title":"(.*?)"', expand=False).value_counts().to_dict()
    return music_dict


# --------------------  voice --------------------------------------

def voice_time_distribution(df):
    '''所有用户，0-3点、3-6点、6-9点、9-12点、
       12-15点、15-18点、18-21点、21-24点的语音使用人数占比
    '''
    # __author__:libin
    # __datetime__:2018-11-15,17:11
    # 默认传进来的DataFrame可以直接使用(至少要有uid和server_time两列)，
    # 分成各个小区间，算出uid去重后的个数
    # 输出字典;{3: 36460,6: 89366,...,21: 323012,24: 149788}
    import pandas as pd
    # list for dict
    # [3, 6, 9, 12, 15, 18, 21, 24]
    dict_key_list = [i for i in range(3, 25, 3)]
    dict_value_list = []
    ua_df = df[["uid", "server_time"]]
    ua_df['server_time'] = ua_df['server_time'].map(
        lambda x: time.strftime("%H", time.localtime(x)))
    ua_df['server_time'] = pd.to_numeric(ua_df['server_time'])
    for i in dict_key_list:
        temp_value = len(ua_df[ua_df['server_time'].map(
            lambda x: ((x >= i - 3) and (x < i)))]["uid"].unique())
        dict_value_list.append(temp_value)
    final_dict = dict(zip(dict_key_list, dict_value_list))
    return final_dict


def voice_search_df(df):
    """
        过滤voice(语音)
    """
    return df[(df.uat.isin([UAT_VOICE, UAT_VOICE_REPEAT]))]


def voice_long_df(df):
    """语音打开时长
    这个只针对同一个sessionId时open出现在dismiss前面，
    其余情况一律忽视，会过滤异常值
    11-16改动：预处理uid和client_time双重排序。
    ::return:
                : 平均每个用户每天使用语音的时长，单位为秒
    """
    time_long, last_sessionid, temp_uid, count, last_time, = 0, 0, 0, 1, None
    THRESHOLD = 200  # 脏数据的门限值，正常值的范围在20以内，
    # 这里写成 大于20且小于50万就行
    df_voice_long = df[df.json.str.contains('"type":"window"')]
    df_voice_long.sort_values(by=['uid', 'client_time'], inplace=True)

    for index, record in df_voice_long.iterrows():
        try:
            record_dict = json.loads(record['json'])
            temp_uid = record['uid']
        except Exception:
            continue

        if record_dict['action'] == 'open':
            last_sessionid = record_dict['sessionId']
            last_time = record['client_time']
        if (record_dict['action'] == 'dismiss')and (record['uid'] == temp_uid):
            try:
                temp_count = abs(last_time - record['client_time'])
                if temp_count > THRESHOLD:
                    raise Exception("脏数据，过滤掉")
                time_long += temp_count
            except Exception:
                # 第一个action == dismiss的时候会出错，后面计算的没影响
                continue
    count = len(df_voice_long.uid.unique())
    return time_long // count

# ---------------------------  电台   ----------------------------------------


def scene_audio(df):
    """
    电台相关
    """
    return df[df.json.str.contains('"scene":"audio"')]


def audio_df(df):
    """从keywords中获取电台关键字的各个次数。

    Returns: 
        keywords 中提到的计数。 字典。
    """

    audio_count_dict = Counter()

    df_audio = scene_audio(df)
    for index, record in df_audio.iterrows():
        record_dict = json.loads(record['json'])
        record_model = record_dict.get("model", None)
        if not record_dict:
            continue

        record_keywords = record_model['keywords']
        for keyword in record_keywords:
            audio_count_dict[keyword] += 1

    return audio_count_dict

# ------------------------  车身控制  ----------------------------------------


def voice_control_df(df):
    '''筛选车身控制
    Args:
        param : pandas.DataFrame

    Return:
        车身控制的数量。int
    '''
    ua_df = df[df.json.str.contains('"scene":"airC"|"scene":"command"')].json
    ua_df = ua_df[ua_df.str.contains('空调|风量|温度|除霜|除雾|内循环|外循环|前窗|后窗|天窗')]
    return ua_df.shape[0]


# -----------------------------------------------------------------------------

def scene_unknow(df):
    """无法识别"""
    return df[(df.json.str.contains('"scene":"unknown"') |
               df.json.str.contains('"r":"nul"') |
               df.json.str.contains('"r":"nul"')) &
              ~df.json.str.contains('"answer"')
              ]


def scene_wakeup(df):
    """唤醒"""
    return df[df.json.str.contains('"scene":"wakeup"') |
              df.json.str.contains('"r":"wakeup"')]


def scene_set_wakeup_keywords(df):
    """设置唤醒词"""
    return df[df.json.str.contains('"scene":"set_user_wakeup_keywords"')]


def scene_command(df):
    """执行命令"""
    return df[df.json.str.contains('"scene":"command"') |
              df.json.str.contains('"cmd"')]


def scene_app(df):
    """应用相关"""
    return df[df.json.str.contains('"scene":"app"') |
              df.json.str.contains('"r":"app"')]


def scene_call(df):
    """电话场景"""
    return df[df.json.str.contains('"scene":"call"') |
              df.json.str.contains('"r":"call"')]


def scene_nav(df):
    """导航相关"""
    return df[df.json.str.contains('"scene":"nav"') |
              df.json.str.contains('"r":"nav"')]


def scene_poi(df):
    """poi相关"""
    return df[df.json.str.contains('"scene":"poi"')]


def scene_weather(df):
    """天气相关"""
    return df[df.json.str.contains('"scene":"weather"')]


def scene_stock(df):
    """
    股票相关
    """
    return df[df.json.str.contains('"scene":"stock"')]


def scene_location(df):
    """位置相关"""
    return df[df.json.str.contains('"scene":"location"')]


def scene_traffic(df):
    """
    路况
    """
    return df[df.json.str.contains('"scene":"traffic"')]


def scene_limit(df):
    """限行"""
    return df[df.json.str.contains('"scene":"limit_number"')]


def scene_unsupport(df):
    """不支持操作"""
    return df[df.json.str.contains('"scene":"unsupport"')]


def scene_empty(df):
    """没有说话"""
    return df[df.json.str.contains('"scene":"empty"') |
              df.json.str.contains('"r":"empty"')]


def scene_wechat(df):
    """微信场景"""
    return df[df.json.str.contains('"scene":"wechat"')]


def scene_query(df):
    """查询相关"""
    return df[df.json.str.contains('"scene":"query"')]


def scene_system(df):
    """系统指令"""
    return df[df.json.str.contains('"scene":"system"') |
              df.json.str.contains('"r":"cmd"')]


def scene_fix(df):
    """对上次会话进行更改"""
    return df[df.json.str.contains('"scene":"fix"')]


def scene_txz(df):
    """core相关"""
    return df[df.json.str.contains('"scene":"txz"')]


def scene_radio(df):
    """电台相关"""
    return df[df.json.str.contains('"scene":"radio"')]


def scene_chat(df):
    """闲聊场景"""
    return df[df.json.str.contains('"r":"cmu"') |
              (df.json.str.contains('"scene":"unknown"') &
               df.json.str.contains('"answer"'))]
