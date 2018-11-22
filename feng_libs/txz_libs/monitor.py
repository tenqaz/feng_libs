"""
    与monitor相关
"""
import os

from txz_libs.components import Moment


def unzip_chrono_file(
    startTime, endTime,
    source_path="/txz_user_action_data/txz/logicError",
    aim_path="/home/jim/monitor_data",
):
    '''
    将流水文件复制到自定义目录，再解压取得.le文件
    :param
            source_path: 源数据文件路径
            aim_path: 目标路径
            startTime: 开始时间
            endTime: 结束时间 +1

            return : file_list           *包含三个文件名的列表
    '''

    # 复制文件到自己的目录下
    fileList = [source_path+"/" +
                file.format()+".7z" for file in Moment.range(
                    startTime, endTime
                )]
    files = " ".join(fileList)
    cmd_str = '''cp {files} {aim_path}'''.format(**{
        'files': files,
        'aim_path': aim_path,
    })
    os.system(cmd_str)

    # 解压成3个文件
    for file in Moment.range(startTime, endTime):
        _file = file.format()+".7z"
        cmd_unzip_str = f"7za x {aim_path}/{_file} -o{aim_path}"
        os.system(cmd_unzip_str)
