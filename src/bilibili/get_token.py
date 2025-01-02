import webbrowser
import requests
from urllib.parse import urlencode

# B站OAuth2.0配置
CLIENT_ID = '你的app_key'
CLIENT_SECRET = '你的app_secret'
REDIRECT_URI = 'https://www.bilibili.com'
AUTH_URL = 'https://passport.bilibili.com/oauth2/authorize'
TOKEN_URL = 'https://passport.bilibili.com/oauth2/access_token'

def get_auth_code():
    # 构建授权URL
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'state': 'bilibili_auth'
    }
    auth_url = f"{AUTH_URL}?{urlencode(params)}"
    
    # 打开浏览器进行授权
    print(f"请在浏览器中访问以下URL进行授权：\n{auth_url}")
    webbrowser.open(auth_url)
    
    # 获取授权码
    auth_code = input("授权完成后，请将重定向URL中的code参数值粘贴到这里：")
    return auth_code

def get_access_token(auth_code):
    # 获取access_token
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    else:
        raise Exception(f"获取access_token失败：{response.text}")

if __name__ == '__main__':
    # 获取授权码
    auth_code = get_auth_code()
    
    # 获取access_token
    access_token = get_access_token(auth_code)
    print(f"成功获取access_token：{access_token}")
