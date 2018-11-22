import time


def strtime2timestamp(str, format="%Y-%m-%d %H:%M:%S"):
    '''
        按照一定的格式，将字符串时间转换成时间戳
    '''
    return int(time.mktime(time.strptime(str, format)))


if __name__ == "__main__":
    timestamp = strtime2timestamp("2018-09-09 1:1:1")
    print(timestamp)
