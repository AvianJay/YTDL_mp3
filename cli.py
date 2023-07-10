import argparse
import os
import json
import ytmp3
import ytpl
from PyQt5.QtWidgets import *
from PyQt5 import uic
from config import config
import sys
import logging


class editor(QMainWindow):
    def __init__(self):
        super(editor, self).__init__()
        uic.loadUi('editor.ui', self)
        self.show()
        self.setWindowTitle('YTDL_mp3 Config Editor')
        self.save.triggered.connect(self.savecfg)
        self.reload.triggered.connect(self.reloadcfg)
        if os.path.exists(os.path.expanduser('~/.ytdl_mp3.cfg.json')):
            with open(os.path.expanduser('~/.ytdl_mp3.cfg.json'), 'r') as f:
                self.editplace.setPlainText(f.read())

    def savecfg(self):
        with open(os.path.expanduser('~/.ytdl_mp3.cfg.json'), 'w') as f:
            f.write(self.editplace.toPlainText())

    def reloadcfg(self):
        with open(os.path.expanduser('~/.ytdl_mp3.cfg.json'), 'r') as f:
            self.editplace.setPlainText(f.read())


def editcfg():
    app = QApplication([])
    ui = editor()
    app.exec_()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(prog=None, usage=None, epilog=None, description='Download YouTube videos and convert them to MP3')
        parser.add_argument('url', help='YouTube video or playlist URL')
        parser.add_argument('-s', '--square', action='store_true', help='Crop thumbnail to square')
        parser.add_argument('-ec', '--edit_config', action='store_true', help='Set Default Settings')
        parser.add_argument('-dcy', '--disable_check_ytdl', action='store_true', help='Disable Check Youtube_dl')
        parser.add_argument('-dcf', '--disable_check_ff', action='store_true', help='Disable Check FFmpeg')
        parser.add_argument('-q', '--quiet', action='store_true', help='Reduce Console Output')
        args = parser.parse_args()

        dl = True

        if args.edit_config:
            dl = False
            editcfg()

        if 'youtube.com' not in args.url and 'youtu.be' not in args.url and dl:
            print('Error: invalid URL')
            exit()

        if args.square:
            config['square'] = args.square

        if 'playlist?list=' in args.url and dl:
            ytpl.downloadplaylist(args.url)
        else:
            ytmp3.downloadmp3(args.url)
    else:
        print('')
