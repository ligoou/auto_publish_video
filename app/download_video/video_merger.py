import os
from .merge_video_subtitles import merge_video_subtitles

class VideoMerger:
    def __init__(self, output_dir='downloads'):
        self.output_dir = output_dir

    def merge(self, video_path, subtitle_path, output_path=None):
        """合并视频和字幕"""
        if output_path is None:
            video_id = os.path.splitext(os.path.basename(video_path))[0].lstrip('f')
            output_path = os.path.join(self.output_dir, f'f{video_id}_with_sub.mp4')
        
        if os.path.exists(video_path) and os.path.exists(subtitle_path):
            merge_video_subtitles(
                os.path.abspath(video_path),
                os.path.abspath(subtitle_path),
                os.path.abspath(output_path)
            )
            return output_path
        return None
