from .controller import YoutubeDownloadController

def download_video_with_subtitles(url: str, output_dir: str = 'downloads') -> dict:
    """
    下载YouTube视频及其字幕，并将字幕翻译为中文
    
    Args:
        url (str): YouTube视频URL
        output_dir (str): 输出目录，默认为'downloads'
    
    Returns:
        dict: 包含下载结果信息的字典
    """
    controller = YoutubeDownloadController(output_dir)
    return controller.download_video_with_subtitles(url)

if __name__ == '__main__':
    # 示例用法
    url = 'https://www.youtube.com/watch?v=yFwV3Ra50e8' #input("请输入YouTube视频URL: ")
    result = download_video_with_subtitles(url, 'downloads')
    print("\n下载结果:")
    print(result)
