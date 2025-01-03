import subprocess

def merge_video_subtitles(video_path, subtitle_path, output_path):
    # 处理路径中的特殊字符
    subtitle_path = subtitle_path.replace('\\', '/').replace(':', '\\:')
    
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-vf', f"subtitles='{subtitle_path}':force_style='Fontsize=24,PrimaryColour=&H000000,OutlineColour=&HFFFFFF,BackColour=black'",
        '-c:v', 'libx264',
        '-c:a', 'copy',
        output_path
    ]
    
    try:
        print("正在执行命令:", ' '.join(command))
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        print(f"视频和字幕合并成功，结果已保存到 {output_path}")
        print("命令输出:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"合并失败，返回码: {e.returncode}")
        print("错误输出:", e.stderr)
    except FileNotFoundError:
        print("未找到ffmpeg，请确保已安装ffmpeg并添加到系统PATH")
    except Exception as e:
        print(f"发生未知错误: {str(e)}")

if __name__ == "__main__":
    video_path = 'E:\\workspace_py\\auto_publish_video\\downloads\\fdge4DhKDdR8.mp4'
    subtitle_path = 'E:\\workspace_py\\auto_publish_video\\downloads\\fdge4DhKDdR8_en_zh-cn.srt'
    output_path = 'E:\\workspace_py\\auto_publish_video\\downloads\\fdge4DhKDdR8_with_sub.mp4'
    merge_video_subtitles(video_path, subtitle_path, output_path)
