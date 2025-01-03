import os
from yt_dlp import YoutubeDL
import logging

class YoutubeDownloader:
    
    
    def __init__(self, output_dir='downloads'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.output_dir, 'f%(id)s.%(ext)s'),
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'en-US', 'en-GB'],
            'subtitlesformat': 'srt',
            'skip_download': False,
            'ignoreerrors': False,
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'force_generic_extractor': False,
            'cookiefile': 'cookie.txt',
            'retries': 10,
            'sleep_interval': 5,
            'postprocessors': [
                {
                    'key': 'FFmpegSubtitlesConvertor',
                    'format': 'srt',
                    'when': 'before_dl',
                },
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }
            ],
        }

    def get_video_info(self, url):
        """获取视频信息"""
        with YoutubeDL(self.ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    def download(self, url):
        """下载视频和字幕"""
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        logger.info(f"Current file location: {os.path.abspath(__file__)}")

        with YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])
            return os.path.join(self.output_dir, f'f{self.get_video_info(url)["id"]}.mp4')
