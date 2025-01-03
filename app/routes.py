# app/routes.py
from flask import render_template, request, jsonify
from app import app
from app.download_video.controller import YoutubeDownloadController

download_controller = YoutubeDownloadController()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/down')
def down():
    return render_template('down.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    result = download_controller.download_video_with_subtitles(url)
    if result.get('status') == 'success':
        return jsonify({
            'success': True,
            'message': '视频下载并合并成功',
            'data': result
        })
    else:
        return jsonify({
            'success': False,
            'message': result.get('message', '下载失败')
        })
