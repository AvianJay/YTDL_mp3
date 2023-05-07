CONFIG_FILE = os.path.expanduser('~/.ytdl_mp3.cfg.json')
DEFAULT_CONFIG = {
    'thumbnail': 'default',
    'check_ytdl': True,
    'check_ffmpeg': True,
    'quiet': False
}
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
else:
    config = DEFAULT_CONFIG
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)