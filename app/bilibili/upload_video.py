import requests
import json
from datetime import datetime

class BilibiliUploader:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = 'https://api.bilibili.com'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

    def upload_video(self, video_path, title, description, tags, category):
        """
        上传视频到B站
        :param video_path: 视频文件路径
        :param title: 视频标题
        :param description: 视频描述
        :param tags: 视频标签列表
        :param category: 视频分类
        :return: 视频发布结果
        """
        # 1. 获取上传凭证
        upload_info = self._get_upload_info()
        
        # 2. 上传视频文件
        video_url = self._upload_file(video_path, upload_info)
        
        # 3. 提交视频信息
        return self._submit_video_info(video_url, title, description, tags, category)

    def _get_upload_info(self):
        """获取视频上传凭证"""
        url = f'{self.base_url}/x/video/upload/info'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()['data']
        else:
            raise Exception(f"获取上传凭证失败：{response.text}")

    def _upload_file(self, file_path, upload_info):
        """上传视频文件"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                upload_info['url'],
                files=files,
                data=upload_info['params']
            )
            if response.status_code == 200:
                return response.json()['data']['url']
            else:
                raise Exception(f"视频上传失败：{response.text}")

    def _submit_video_info(self, video_url, title, description, tags, category):
        """提交视频信息"""
        url = f'{self.base_url}/x/video/add'
        data = {
            'title': title,
            'desc': description,
            'tag': ','.join(tags),
            'category': category,
            'source': video_url,
            'copyright': 1,  # 1表示原创，2表示转载
            'tid': 76,  # 默认分区：生活
            'cover': '',  # 封面图URL
            'dtime': int(datetime.now().timestamp())  # 定时发布时间
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"视频发布失败：{response.text}")

if __name__ == '__main__':
    # 示例用法
    access_token = '你的access_token'
    uploader = BilibiliUploader(access_token)
    
    try:
        result = uploader.upload_video(
            video_path='example.mp4',
            title='测试视频',
            description='这是一个测试视频',
            tags=['测试', '示例'],
            category=76
        )
        print(f"视频发布成功：{result}")
    except Exception as e:
        print(f"视频发布失败：{str(e)}")
