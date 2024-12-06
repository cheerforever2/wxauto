import configparser
import os
import shutil
import time
import sys
from datetime import datetime
from chinese_calendar import is_workday
from chinese_calendar import get_holidays

# 将wxauto源码目录添加到系统路径中，以便能够正确导入其中的模块
sys.path.append(os.path.abspath('wxauto'))

# 从wxauto源码中的相关模块引入需要的类和函数
from wxauto import WeChat

# 读取配置文件
def read_config():
    config = configparser.ConfigParser()
    config.read('backup_config.ini', encoding='utf-8')
    return config


# 备份今日聊天媒体文件并记录相关信息（使用wxauto库）
def backup_today_chat_media(chat_name, backup_base_dir):
    wechat = WeChat()

    # 获取当前日期和时间
    current_date_time = datetime.now()
    current_date = current_date_time.strftime('%Y%m%d')
    current_time = current_date_time.strftime('%H:%M:%S')

    # 创建以当前日期命名的备份目录（先检查是否已存在）
    backup_dir = os.path.join(backup_base_dir, current_date)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)

    # 用于统计图片和视频数量以及总容量
    pic_count = 0
    video_count = 0
    total_size = 0

    # 查找聊天对象
    chat_object = wechat.ChatWith(chat_name)[0]
    wechat.LoadMoreMessage()

    # 获取聊天记录
    msgs = wechat.GetTodayMessage(
    savepic   = True,
    savevideo = True)

# 管理日志文件大小，保持大致一个月的记录量（从第一行开始搜找到第一个满足一个月之内的行，删除前面的）
def manage_log_file_size(log_file_path):
    one_month_seconds = 30 * 24 * 60 * 60
    current_time_seconds = time.time()

    with open(log_file_path, 'r', encoding='gbk') as f:
        lines = f.readlines()

    delete_start_index = None
    for i, line in enumerate(lines):
        line_time_str = line.split(' - ')[0]
        line_time = datetime.strptime(line_time_str[:-7], '%Y-%m-%d %H:%M:%S')
        line_time_seconds = time.mktime(line_time.timetuple())
        if current_time_seconds - line_time_seconds < one_month_seconds:
            delete_start_index = i
            break

    if delete_start_index is not None:
        lines = lines[delete_start_index:]

    with open('backup_log.txt', 'w', encoding='gbk') as f:
        f.writelines(lines)

if __name__ == "__main__":
    config = read_config()

    # 从配置文件获取要备份的微信对话名称和备份基础目录
    target_chat_name = config.get('BackupSettings', 'chat_name')
    backup_base_dir = config.get('BackupSettings', 'backup_base_dir')

    # 备份今日聊天媒体文件并记录相关信息
    if is_workday(datetime.now().date()):
        backup_today_chat_media(target_chat_name, backup_base_dir)
    else:
        log_file_path = "backup_log.txt"
        with open(log_file_path, 'a', encoding='gbk') as f:
            f.write(f"{datetime.now()} - 不是法定工作日，不执行备份\n")

    # 管理日志文件大小
    manage_log_file_size("backup_log.txt")