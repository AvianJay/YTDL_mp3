import os
import json
import re
import sys

CONFIG_FILE = os.path.expanduser('~/.ytdl_mp3.cfg.json')
DEFAULT_CONFIG = {
    'square': False,
    'check_ytdl': True,
    'check_ffmpeg': True,
    'quiet': False,
    'config_version': 2
}


def update_config(cfg):
    if 'quiet' not in cfg or not cfg['quiet']:
        print(f'Updating Config to Version{DEFAULT_CONFIG["config_version"]}!')
    if 'square' not in cfg:
        cfg['square'] = DEFAULT_CONFIG['square']
    if 'quiet' not in cfg:
        cfg['quiet'] = DEFAULT_CONFIG['quiet']
    if 'check_ytdl' not in cfg:
        cfg['check_ytdl'] = DEFAULT_CONFIG['check_ytdl']
    if 'check_ffmpeg' not in cfg:
        cfg['check_ffmpeg'] = DEFAULT_CONFIG['check_ffmpeg']
    cfg['config_version'] = DEFAULT_CONFIG['config_version']
    return cfg


if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        if not config['config_version'] or config['config_version'] < DEFAULT_CONFIG['config_version']:
            new_config = update_config(config)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(new_config, f)
    except:
        print('Your Config is Excepted,Delete ' + CONFIG_FILE + ' yourself or edit it.')
        sys.exit(1)
else:
    config = DEFAULT_CONFIG
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


def legalize_filename(filename):
    # 文件名合法化，參考https://github.com/miyouzi/aniGamerPlus/blob/master/Config.py的48到59行
    legal_filename = re.sub(r'\|+', '｜', filename)  # 处理 | , 转全型｜
    legal_filename = re.sub(r'\?+', '？', legal_filename)  # 处理 ? , 转中文 ？
    legal_filename = re.sub(r'\*+', '＊', legal_filename)  # 处理 * , 转全型＊
    legal_filename = re.sub(r'<+', '＜', legal_filename)  # 处理 < , 转全型＜
    legal_filename = re.sub(r'>+', '＞', legal_filename)  # 处理 < , 转全型＞
    legal_filename = re.sub(r'\"+', '＂', legal_filename)  # 处理 " , 转全型＂
    legal_filename = re.sub(r':+', '：', legal_filename)  # 处理 : , 转中文：
    legal_filename = re.sub(r'\\', '＼', legal_filename)  # 处理 \ , 转全型＼
    legal_filename = re.sub(r'/', '／', legal_filename)  # 处理 / , 转全型／
    return legal_filename
