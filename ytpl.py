from youtubesearchpython import *
import os
import ytmp3
import sys
import re
import json
import config
from tqdm import tqdm


def dl(playlist):
  try:
    os.mkdir(config.legalize_filename(playlist['info']['title']))
    os.chdir(config.legalize_filename(playlist['info']['title']))
  except:
    os.mkdir(config.legalize_filename(playlist['info']['title']) + '(2)')
    os.chdir(config.legalize_filename(playlist['info']['title']) + '(2)')
  with open(config.legalize_filename(playlist['info']['title']) + '.m3u8', 'w') as f:
    f.write('#EXTM3U\n')
  progress_bar = tqdm(total=len(playlist['videos']))
  counter = 0
  for video in playlist['videos']:
    progress_bar.update(1)
    counter = counter + 1
    content = ytmp3.downloadmp3('https://www.youtube.com/watch?v=' + video['id'], track_id=counter)
    with open(playlist['info']['title'] + '.m3u8', 'a') as f:
      f.write('#EXTINF:-1,' + content['title'] + '\n' + content['filename'] + '\n')
  progress_bar.close()

def downloadplaylist(url):
  playlist = Playlist.get(url)

  print(f'Videos Retrieved: {len(playlist["videos"])}')
  dl(playlist)

if __name__ == '__main__':
  if len(sys.argv) > 1:
    playlist = Playlist.get(sys.argv[1])

    print(f'Videos Retrieved: {len(playlist["videos"])}')
    
    dl(playlist)
