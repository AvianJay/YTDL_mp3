import argparse
import os
import json
import ytmp3
import ytpl
from PyQt5.QtWidgets import *
from PyQt5 import uic
from config import config

class editor(QMainWindow):
    def __init__(self):
        super(editor, self).__init__()
        uic.loadUi('editor.ui', self)
        self.show()
        self.setWindowTitle('YTDL_mp3 Config Editor')
        self.save.triggered.connect(self.save)
        self.reload.triggered.connect(self.reload)
        if os.path.exists(os.path.expanduser('~/.ytdl_mp3.cfg.json')):
            with open(os.path.expanduser('~/.ytdl_mp3.cfg.json'), 'r') as f:
                self.editplace(f.read())

    def save(self):
        with open(os.path.expanduser('~/.ytdl_mp3.cfg.json'), 'w') as f:
            f.write(self.editplace.toPlainText())

    def reload(self):
        with open(os.path.expanduser('~/.ytdl_mp3.cfg.json'), 'r') as f:
            self.editplace(f.read())

def editcfg():
    print('')

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Download YouTube videos and convert them to MP3')
    parser.add_argument('url', help='YouTube video or playlist URL')
    parser.add_argument('-t', '--thumbnail', metavar='THUMBNAIL_URL', help='thumbnail URL')
    parser.add_argument('-sd', '--set_default', action='store_true', help='Set Default Settings')
    parser.add_argument('-dcy', '--disable_check_ytdl', action='store_true', help='Disable Check Youtube_dl')
    parser.add_argument('-dcf', '--disable_check_ff', action='store_true', help='Disable Check FFmpeg')
    parser.add_argument('-q', '--quiet', action='store_true', help='Reduce Console Output')
    args = parser.parse_args()

    if args.set_default:
        dl = False

    if 'youtube.com' not in args.url and 'youtu.be' not in args.url and dl:
        print('Error: invalid URL')
        exit()

    if args.thumbnail:
        config['thumbnail'] = args.thumbnail

    if 'playlist?list=' in args.url and dl:
        ytpl.download_playlist(args.url, config)
    else:
        ytmp3.download_mp3(args.url, config)

