from youtubesearchpython import *
import os
import ytmp3
import sys
import re
import json

CONFIG_FILE = os.path.expanduser('~/.ytdl_mp3.cfg.json')
DEFAULT_CONFIG = {
    'thumbnail': 'default'
}

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
else:
    config = DEFAULT_CONFIG
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def dl(playlist, config):
  try:
    os.mkdir(playlist['info']['title'])
    os.chdir(playlist['info']['title'])
  except:
    os.mkdir(playlist['info']['title'] + '(2)')
    os.chdir(playlist['info']['title'] + '(2)')
  with open(playlist['info']['title'] + '.m3u8', 'w') as f:
    f.write('#EXTM3U\n')
  counter = 0
  for video in playlist['videos']:
    counter = counter + 1
    content = ytmp3.downloadmp3('https://www.youtube.com/watch?v=' + video['id'], track_id=counter)
    with open(playlist['info']['title'] + '.m3u8', 'a') as f:
      f.write('#EXTINF:-1,' + content['title'] + '\n' + content['filename'] + '\n')

def downloadplaylist(url, cfg=config):
  playlist = Playlist.get(url)

  print(f'Videos Retrieved: {len(playlist["videos"])}')
  print('Found all the videos.')

  dl(playlist, cfg)

if __name__ == '__main__':
  if len(sys.argv) > 1:
    playlist = Playlist.get(sys.argv[1])

    print(f'Videos Retrieved: {len(playlist["videos"])}')
    print('Found all the videos.')
    
    dl(playlist, config)
