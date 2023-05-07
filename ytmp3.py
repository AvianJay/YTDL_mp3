import os
import sys
from moviepy.editor import *
import requests
import re
from PIL import Image
from io import BytesIO
from mutagen.id3 import ID3, APIC, TIT2, TPE1, error, TALB, TRCK
import json
import subprocess
import importlib
import ctypes
import config

if config.config['checkytdl']:
    if not config.config['quiet']:
        print("Notify: Started Checking Youtube_dl, Use -dcy or --disable-check-ytdl to Disable checking Youtube_dl.")
    try:
        import youtube_dl

        got = False
        try:
            y = {'quiet': True, 'skip_download': True, 'forcetitle': True, 'forcejson': True, 'noplaylist': True}
            with youtube_dl.YoutubeDL(y) as ydl:
                info = ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)
                got = True
        except:
            got = False
        if not got:
            subprocess.run(['pip', 'uninstall', 'youtube_dl', '-y'])
            subprocess.run(['pip', 'install', 'https://github.com/ytdl-org/youtube-dl/archive/refs/heads/master.zip'])
            importlib.reload(youtube_dl)
    except:
        subprocess.run(['pip', 'install', 'https://github.com/ytdl-org/youtube-dl/archive/refs/heads/master.zip'])
        import youtube_dl

        importlib.reload(youtube_dl)
else:
    import youtube_dl

# 定义要执行的 ffmpeg 命令
ffmpeg_cmd = ["ffmpeg", "-version"]

# 执行 ffmpeg 命令
if config.config['checkffmpeg']:
    if not config.config['quiet']:
        print("Notify: Started Checking FFmepg, Use -dcf or --disable-check-ff to Disable checking FFmepg.")
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        output = result.stdout
        # 检查输出中是否包含 ffmpeg 版本信息
        if not "ffmpeg version" in output and not config.config['quiet']:
            print("WARNING: ffmpeg is not executable.")
    except FileNotFoundError:
        print('ERROR: FFmpeg is not found')
        print('Please Install FFmpeg Manually Before using ytdl_mp3.')
        sys.exit(1)
    try:
        result = subprocess.run(["ffprobe", "-version"], capture_output=True, text=True)
        output = result.stdout
        # 检查输出中是否包含 ffmpeg 版本信息
        if not "ffprobe version" in output and config.config['quiet']:
            print("WARNING: FFprobe is not executable.")
    except FileNotFoundError:
        print('ERROR: FFprobe is not found')
        print('Please Install FFprobe Manually Before using ytdl_mp3.')
        sys.exit(1)

# 从YouTube下载视频并将其转换为MP3文件
def download_and_convert_to_mp3(video_url, title):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': title + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info)
    if ".m4a" in filename:
        filename = filename.replace(".m4a", ".mp3")
    elif ".webm" in filename:
        filename = filename.replace(".webm", ".mp3")
    elif ".mp4" in filename:
        filename = filename.replace(".mp4", ".mp3")
    return filename

# 从YouTube获取视频标题、艺术家和图像
def get_youtube_metadata(video_url, config):
    metadata = {}
    ydl_opts = {'quiet': True, 'skip_download': True, 'forcetitle': True, 'forcejson': True, 'noplaylist': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(video_url, download=False)
        if not result.get('track', 1) == 1:
            metadata['title'] = result.get('track')
        elif not result.get('alt_title', 1) == 1:
            metadata['title'] = result.get('alt_title')
        else:
            metadata['title'] = result.get('title', 'Untitled')
        if result.get('artist', 1) == 1:
            metadata['artist'] = result.get('channel', 'Unknown Channel')
        else:
            metadata['artist'] = result.get('artist')
        if not result.get('album', 1) == 1:
            metadata['album'] = result.get('album')
        if not result.get('thumbnails', 1) == 1:
            thumbnails = result.get('thumbnails')
            # 以畫質作為 key，儲存 url
            urls_by_resolution = {}
            for thumbnail in thumbnails:
                urls_by_resolution[thumbnail['resolution']] = thumbnail['url']

            # 取得最高畫質
            resolutions = [thumbnail['resolution'] for thumbnail in thumbnails]
            highest_resolution = sorted(resolutions)[-1]

            # 取得最高畫質的 url
            highest_resolution_url = urls_by_resolution[highest_resolution]
            if config['thumbnail'] == 'square':
                response = requests.get(highest_resolution_url)
                thumbnail_data = response.content
                thumbnail = Image.open(BytesIO(thumbnail_data))
                thumbnail = thumbnail.crop((0, 0, min(thumbnail.size), min(thumbnail.size)))
                output_buffer = BytesIO()
                thumbnail.save(output_buffer, format='JPEG')
                metadata['thumbnail'] = output_buffer.getvalue()
            else:
                metadata['thumbnail'] = requests.get(highest_resolution_url).content
    return metadata

# 将元数据添加到MP3文件中
def add_metadata_to_mp3(file_path, metadata):
    audio = ID3(file_path)
    try:
        audio.add(TIT2(encoding=3, text=metadata['title']))
        audio.add(TPE1(encoding=3, text=metadata['artist']))
        if 'thumbnail' in metadata:
            audio.add(APIC(3, 'image/jpeg', 3, 'Front cover', metadata['thumbnail']))
        if 'album' in metadata:
            audio.add(TALB(encoding=3, text=metadata['album']))
        if 'track_id' in metadata:
            audio.add(TRCK(encoding=3, text=metadata['track_id']))
        audio.save()
    except error:
        pass

def downloadmp4(video_url, cfg=config.config):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'preferredcodec': 'mp4',
        }],
    }
    if cfg['quiet']:
        ydl_opts['quiet'] = True
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info)
    return filename

def downloadmp3(url, cfg=config.config, track_id=1):
  lc = r'[\\/*:?<>|"]'
  metadata = get_youtube_metadata(url, cfg)
  content = {}
  content['title'] = metadata['title']
  content['filename'] = re.sub(lc, '' ,metadata['title']) + '.mp3'
  file_path = download_and_convert_to_mp3(url, re.sub(lc, '', metadata['title']))
  print(file_path)
  content[file_path] = file_path
  if track_id:
    metadata['track_id'] = str(track_id)
  add_metadata_to_mp3(file_path, metadata)
  return content

if __name__ == '__main__':
  if len(sys.argv) > 1:
    video_url = sys.argv[1]
    downloadmp3(video_url, cfg=config.config)
