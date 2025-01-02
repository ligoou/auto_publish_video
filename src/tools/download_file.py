import requests
from tqdm import tqdm


def download_file_with_progress(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        with open(save_path, 'wb') as file, tqdm(
            desc=save_path,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))
        print(f"文件已保存到 {save_path}")
    except Exception as e:
        print(f"下载失败: {e}")