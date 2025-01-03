function downloadVideo() {
    const videoUrl = document.getElementById('videoUrl').value;
    const status = document.getElementById('status');
    
    if (!videoUrl) {
        status.textContent = '请输入YouTube视频链接';
        return;
    }

    status.textContent = '正在处理...';

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: videoUrl })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            status.textContent = '视频下载并合并成功！';
        } else {
            status.textContent = '处理失败：' + data.message;
        }
    })
    .catch(error => {
        status.textContent = '发生错误：' + error.message;
    });
}
