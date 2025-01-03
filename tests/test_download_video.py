import unittest
from unittest.mock import patch
from app.download_video import (
    YoutubeDownloader,
    SubtitleProcessor,
    VideoMerger,
    YoutubeDownloadController
)

class TestYoutubeDownloader(unittest.TestCase):
    @patch('yt_dlp.YoutubeDL')
    def test_get_video_info(self, mock_ydl):
        # 测试获取视频信息
        mock_instance = mock_ydl.return_value
        mock_instance.extract_info.return_value = {
            'id': 'test123',
            'title': 'Test Video',
            'duration': 120,
            'view_count': 1000,
            'uploader': 'Test User'
        }
        
        downloader = YoutubeDownloader()
        info = downloader.get_video_info('https://youtube.com/test')
        
        self.assertEqual(info['id'], 'test123')
        self.assertEqual(info['title'], 'Test Video')
        mock_instance.extract_info.assert_called_once_with('https://youtube.com/test', download=False)

class TestSubtitleProcessor(unittest.TestCase):
    @patch('deep_translator.GoogleTranslator')
    def test_process_subtitles(self, mock_translator):
        # 测试字幕处理
        mock_instance = mock_translator.return_value
        mock_instance.translate.side_effect = lambda x: f"Translated {x}"
        
        processor = SubtitleProcessor()
        subtitles = {'en': 'test.srt'}
        
        with patch('builtins.open', unittest.mock.mock_open(read_data='Line 1\nLine 2\n')):
            result = processor.process_subtitles('test123', subtitles)
            
            self.assertIn('en', result)
            self.assertTrue(result['en']['translated'].endswith('_zh-cn.srt'))
            mock_instance.translate.assert_called()

class TestVideoMerger(unittest.TestCase):
    @patch('src.download_video.merge_video_subtitles')
    def test_merge(self, mock_merge):
        # 测试视频合并
        merger = VideoMerger()
        result = merger.merge('video.mp4', 'subtitle.srt')
        
        self.assertIsNotNone(result)
        mock_merge.assert_called_once()

class TestYoutubeDownloadController(unittest.TestCase):
    @patch('src.download_video.YoutubeDownloader')
    @patch('src.download_video.SubtitleProcessor')
    @patch('src.download_video.VideoMerger')
    def test_download_video_with_subtitles(self, mock_merger, mock_processor, mock_downloader):
        # 测试完整流程
        mock_downloader.return_value.get_video_info.return_value = {
            'id': 'test123',
            'title': 'Test Video',
            'requested_subtitles': {'en': {}}
        }
        mock_downloader.return_value.download.return_value = 'video.mp4'
        mock_processor.return_value.process_subtitles.return_value = {
            'en': {'translated': 'subtitle.srt'}
        }
        mock_merger.return_value.merge.return_value = 'final_video.mp4'
        
        controller = YoutubeDownloadController()
        result = controller.download_video_with_subtitles('https://youtube.com/test')
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['video_path'], 'final_video.mp4')

if __name__ == '__main__':
    unittest.main()
