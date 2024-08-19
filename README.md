<div align="center">
    <p align="center">
        <img src="https://github.com/user-attachments/assets/2120ff94-8c29-41ff-8814-341137e026d1" alt="logo" width="200" />
    </p>
    
![GitHub License](https://img.shields.io/github/license/electronic-pig/SmartEditor)
![node.js version](https://img.shields.io/badge/python-3.8+-orange.svg)
![GitHub Repo stars](https://img.shields.io/github/stars/electronic-pig/SmartEditor)

<h1 align="center">妙笔 · 智能编辑器</h1>
</div>

# ✨ 简介

**妙笔** —— 基于大小模型的在线文档富文本编辑器

> 2024年中国软件杯A10赛题

后端仓库请移步[SmartEditor](https://github.com/electronic-pig/SmartEditor)

# 🎉 特性

## 整体功能

- 用户认证
- 文档管理
- 富文本编辑
- AI功能
  
## 赛题要求

- 智能润色
- 多媒体信息提取
- 智能格式排版

# 🛠 技术栈

<table>
    <tr>
        <td align="center">flask</td>
        <td align="center">mysql</td>
        <td align="center">redis</td>
        <td align="center">jwt</td>
        <td align="center">erniebot</td>
        <td align="center">paddlepaddle</td>
    </tr>
    <tr>
        <td align="center">
            <a title="flask" href="https://flask.palletsprojects.com/en/3.0.x/" target="_blank">
                <img height="64px" src="https://github.com/user-attachments/assets/e1ff55a9-f0ff-475d-8aef-82389bc5ebcc"/>
            </a>
        </td>
        <td align="center">
            <a title="mysql" href="https://www.mysql.com/cn/" target="_blank">
                <img height="64px" src="https://github.com/user-attachments/assets/55d8be2b-18bb-4092-b557-fea3e8a7eef1"/>
            </a>
        </td>
        <td align="center">
            <a title="redis" href="https://redis.io/" target="_blank">
                <img height="64px" src="https://github.com/user-attachments/assets/1e7eeaea-677e-4c46-a1fc-977a70857d89"/>
            </a>
        </td>
        <td align="center">
            <a title="jwt" href="https://jwt.io/" target="_blank">
                <img height="64px" src="https://github.com/user-attachments/assets/7ba63fb8-835e-4f28-8cf9-16e51b07127e"/>
            </a>
        </td>
        <td align="center">
            <a title="erniebot" href="https://ernie-bot-agent.readthedocs.io/zh-cn/stable/" target="_blank">
                <img height="64px" src="https://github.com/user-attachments/assets/81a50ba6-eeae-48bf-9663-94284b9b3c4d"/>
            </a>
        </td>
        <td align="center">
            <a title="paddlepaddle" href="https://aistudio.baidu.com/overview" target="_blank">
                <img height="64px" src="https://github.com/user-attachments/assets/93a555e1-83d0-4d0d-8042-1353aea65e97"/>
            </a>
        </td>
    </tr>
</table>

# 🚀 运行
### 配置环境变量
在项目根目录创建并编辑`.env`文件，填写相应的变量值
```bash
SQLALCHEMY_DATABASE_URI = <your_mysql_uri>
REDIS_DATABASE_URI = <your_reids_uri>
MAIL_USERNAME = <your_qqmail_number>
MAIL_PASSWORD = <your_qqmail_server_password>
JWT_SECRET = <any_secret>
ACCESS_TOKEN = <your_baidu_access_token>
OCR_API_URL = <your_baidu_ocr_api_url>
```
### 安装依赖
```sh
pip install -r requirements.txt
```
### 项目运行
```sh
python run.py
```
# 📐 系统架构
![image](https://github.com/user-attachments/assets/cdf5d549-6873-407c-bc39-3884f3a0a930)

# 📄 写在最后
项目制作不易，如果它对你有帮助的话，请务必给作者点一个免费的⭐，万分感谢!🙏🙏🙏
