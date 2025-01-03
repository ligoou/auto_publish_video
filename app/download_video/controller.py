import os
from .youtube_downloader import YoutubeDownloader
from .subtitle_processor import SubtitleProcessor
from .video_merger import VideoMerger

class YoutubeDownloadController:
    def __init__(self, output_dir='downloads'):
        self.output_dir = output_dir
        self.downloader = YoutubeDownloader(output_dir)
        self.subtitle_processor = SubtitleProcessor(output_dir)
        self.video_merger = VideoMerger(output_dir)

    def download_video_with_subtitles(self, url):
        """下载视频并处理字幕"""
        try:
            # 获取视频信息
            info_dict = self.downloader.get_video_info(url)
            video_id = info_dict.get('id', '')
            video_title = info_dict.get('title', '')
            
            # 下载视频
            video_path = self.downloader.download(url)
            
            # 处理字幕
            subtitles = {
                lang_code: os.path.join(self.output_dir, f'f{video_id}.{lang_code}.srt')
                for lang_code in info_dict.get('requested_subtitles', {})
            }
            processed_subs = self.subtitle_processor.process_subtitles(video_id, subtitles)
            
            # 合并视频和字幕
            final_video_path = None
            if processed_subs and os.path.exists(video_path):
                subtitle_path = list(processed_subs.values())[0]['translated']
                final_video_path = self.video_merger.merge(video_path, subtitle_path)
            
            return {
                'status': 'success',
                'video_path': final_video_path if final_video_path else video_path,
                'subtitles': processed_subs,
                'id': video_id,
                'title': video_title,
                'duration': info_dict.get('duration', 0),
                'views': info_dict.get('view_count', 0),
                'author': info_dict.get('uploader', '')
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
