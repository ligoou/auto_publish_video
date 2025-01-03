# B站API凭证获取指南

## 1. 注册B站开放平台开发者账号
1. 访问 [B站开放平台](https://openhome.bilibili.com/)
2. 点击"立即接入"，使用B站账号登录
3. 完成开发者认证

## 2. 创建应用
1. 登录后进入"开发者中心"
2. 点击"创建应用"
3. 选择应用类型（建议选择"个人应用"）
4. 填写应用信息：
   - 应用名称：视频发布工具
   - 应用简介：用于自动发布视频到B站
   - 应用分类：工具类
   - 回调地址：https://www.bilibili.com
5. 提交审核（个人应用通常即时通过）

## 3. 获取API凭证
1. 应用创建成功后，进入"应用管理"
2. 在"基本信息"中获取：
   - App Key
   - App Secret
3. 将这两个值填入get_token.py文件中的CLIENT_ID和CLIENT_SECRET

## 4. 运行脚本获取access_token
1. 安装依赖：
   ```bash
   pip install requests
   ```
2. 运行脚本：
   ```bash
   python src/bilibili/get_token.py
   ```
3. 按照提示完成授权流程
4. 脚本将输出access_token，请妥善保存
