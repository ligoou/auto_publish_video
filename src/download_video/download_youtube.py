import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))
from yt_dlp import YoutubeDL
from deep_translator import GoogleTranslator

def download_video_with_subtitles(url: str, output_dir: str = 'downloads') -> dict:
    """
    下载YouTube视频及其字幕，并将字幕翻译为中文
    
    Args:
        url (str): YouTube视频URL
        output_dir (str): 输出目录，默认为'downloads'
    
    Returns:
        dict: 包含下载结果信息的字典
    """
    try:
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # yt-dlp配置
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_dir, 'f%(id)s.%(ext)s'),
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
            'cookiefile': os.path.join(os.path.dirname(__file__), '..', 'cookie.txt'),
            'retries': 10,
            'sleep_interval': 5,
            'postprocessors': [
                {
                    'key': 'FFmpegSubtitlesConvertor',
                    'format': 'srt',
                    'when': 'before_dl',  # 在下载完成后立即转换字幕
                },
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }
            ],
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            # 获取视频信息
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', '')
            video_id = info_dict.get('id', '')
            translator = GoogleTranslator(source='auto', target='zh-CN')
            print(f"正在下载视频: {translator.translate(video_title)}")
            
            # 下载视频和字幕
            ydl.download([url])

            # 处理字幕翻译
            subtitles = {}
            for lang_code, sub in info_dict.get('requested_subtitles', {}).items():
                sub_path = os.path.join(output_dir, f'f{video_id}.{lang_code}.srt')
                translated_sub_path = os.path.join(output_dir, f'f{video_id}_{lang_code}_zh-cn.srt')

                if os.path.exists(sub_path) and not os.path.exists(translated_sub_path):
                    print(f"处理字幕文件: {sub_path}")
                    with open(sub_path, 'r', encoding='utf-8') as f:
                        original_sub = f.read()
                    
                    # 逐行翻译字幕，增加重试机制
                    translated_lines = []
                    max_retries = 3
                    retry_delay = 1  # 秒
                    seen_lines = set()

                    for line in original_sub.split('\n'):
                                # 如果当前行已经处理过，则跳过
                        if line in seen_lines:
                            continue
                        seen_lines.add(line)

                        if line.strip() and not line.strip().isdigit() and '-->' not in line:
                            retry_count = 0
                            while retry_count < max_retries:
                                try:
                                    translated_line = translator.translate(line)
                                    translated_lines.append(translated_line)
                                    break
                                except Exception:
                                    retry_count += 1
                                    if retry_count == max_retries:
                                        translated_lines.append(line)  # 如果重试多次仍然失败，保留原文
                                    else:
                                        time.sleep(retry_delay)
                        else:
                            translated_lines.append(line)  # 保留时间戳和空行
                    
                    translated_sub = '\n'.join(translated_lines)
                    
                    # 保存翻译后的字幕
                    with open(translated_sub_path, 'w', encoding='utf-8') as f:
                        f.write(translated_sub)
                    
                subtitles[lang_code] = {
                    'original': sub_path,
                    'translated': translated_sub_path
                }

            # 合并视频和字幕
            from src.download_video.merge_video_subtitles import merge_video_subtitles
            video_path = os.path.join(output_dir, f'f{video_id}.mp4')
            final_video_path = os.path.join(output_dir, f'f{video_id}_with_sub.mp4')

            if subtitles and os.path.exists(video_path):
                print(f"开始合并视频和字幕: {video_path}")
                # 检查字幕文件是否存在
                subtitle_path = list(subtitles.values())[0]['translated']
                if os.path.exists(subtitle_path):
                    # 使用绝对路径
                    merge_video_subtitles(
                        os.path.abspath(video_path),
                        os.path.abspath(subtitle_path),
                        os.path.abspath(final_video_path)
                    )
                    print(f"合并完成: {final_video_path}")
                else:
                    print(f"字幕文件不存在: {subtitle_path}")
            else:
                print(f"视频文件不存在或字幕未下载: {video_path}")
            
            return {
                'status': 'success',
                'video_path': final_video_path if os.path.exists(final_video_path) else video_path,
                'subtitles': subtitles,
                'id': video_id,
                'title': video_title,
                'duration': info_dict.get('duration', 0),
                'views': info_dict.get('view_count', 0),
                'author': info_dict.get('uploader', '')
            }
            
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    # 示例用法
    url = 'https://www.youtube.com/watch?v=yFwV3Ra50e8' #input("请输入YouTube视频URL: ")
    result = download_video_with_subtitles(url)
    print("\n下载结果:")
    print(result)
