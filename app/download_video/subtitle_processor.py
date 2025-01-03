import os
import time
from deep_translator import GoogleTranslator

class SubtitleProcessor:
    def __init__(self, output_dir='downloads'):
        self.output_dir = output_dir
        self.translator = GoogleTranslator(source='auto', target='zh-CN')

    def process_subtitles(self, video_id, subtitles):
        """处理并翻译字幕文件"""
        processed_subs = {}
        
        for lang_code, sub_path in subtitles.items():
            translated_sub_path = os.path.join(self.output_dir, f'f{video_id}_{lang_code}_zh-cn.srt')
            
            if os.path.exists(sub_path) and not os.path.exists(translated_sub_path):
                with open(sub_path, 'r', encoding='utf-8') as f:
                    original_sub = f.read()
                
                translated_lines = []
                max_retries = 3
                retry_delay = 1
                seen_lines = set()

                for line in original_sub.split('\n'):
                    if line in seen_lines:
                        continue
                    seen_lines.add(line)

                    if line.strip() and not line.strip().isdigit() and '-->' not in line:
                        retry_count = 0
                        while retry_count < max_retries:
                            try:
                                translated_line = self.translator.translate(line)
                                translated_lines.append(translated_line)
                                break
                            except Exception:
                                retry_count += 1
                                if retry_count == max_retries:
                                    translated_lines.append(line)
                                else:
                                    time.sleep(retry_delay)
                    else:
                        translated_lines.append(line)
                
                translated_sub = '\n'.join(translated_lines)
                
                with open(translated_sub_path, 'w', encoding='utf-8') as f:
                    f.write(translated_sub)
                
                processed_subs[lang_code] = {
                    'original': sub_path,
                    'translated': translated_sub_path
                }
        
        return processed_subs
