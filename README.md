<div align="center">
    <p align="center">
        <img src="https://github.com/user-attachments/assets/a03b2461-b038-4c51-9b30-281987c540be" alt="logo" width="200" />
    </p>
    <h1 align="center">妙笔 · 智能编辑器</h1>
    
![GitHub License](https://img.shields.io/github/license/electronic-pig/SmartEditor_backend)
![python version](https://img.shields.io/badge/python-3.8+-orange.svg)
![GitHub Repo stars](https://img.shields.io/github/stars/electronic-pig/SmartEditor_backend)

</div>

# ✨ 简介

> 2024年中国软件杯A10赛题

妙笔 —— 基于大小模型的在线文档富文本编辑器，通过结合AI技术，为用户提供了一个全面、高效的文档编辑平台。妙笔不仅支持智能润色、多媒体信息提取和智能格式排版等核心功能，还提供了用户友好的交互界面和安全的文档管理体验，极大地提升了内容创作的效率和质量。

前端仓库请移步[SmartEditor](https://github.com/electronic-pig/SmartEditor).

# 🎉 特性

## 核心功能

- 用户认证
- 文档管理
- 富文本编辑
- AI功能
  
## AI辅助

- 智能润色
- 多媒体信息提取
- 智能格式排版

# 🛠 技术栈

| [flask](https://flask.palletsprojects.com/en/3.0.x/) | [mysql](https://www.mysql.com/cn/) | [redis](https://redis.io/) | [jwt](https://jwt.io/) | [erniebot](https://ernie-bot-agent.readthedocs.io/zh-cn/stable/) | [paddlepaddle](https://aistudio.baidu.com/overview) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| [<img src="https://github.com/user-attachments/assets/e1ff55a9-f0ff-475d-8aef-82389bc5ebcc" alt="flask" height="50px"/>](https://flask.palletsprojects.com/en/3.0.x/) | [<img src="https://github.com/user-attachments/assets/55d8be2b-18bb-4092-b557-fea3e8a7eef1" alt="mysql" height="50px"/>](https://www.mysql.com/cn/) | [<img src="https://github.com/user-attachments/assets/1e7eeaea-677e-4c46-a1fc-977a70857d89" alt="redis" height="50px"/>](https://redis.io/) | [<img src="https://github.com/user-attachments/assets/7ba63fb8-835e-4f28-8cf9-16e51b07127e" alt="jwt" height="50px"/>](https://jwt.io/) | [<img src="https://github.com/user-attachments/assets/81a50ba6-eeae-48bf-9663-94284b9b3c4d" alt="erniebot" height="50px"/>](https://ernie-bot-agent.readthedocs.io/zh-cn/stable/) | [<img src="https://github.com/user-attachments/assets/93a555e1-83d0-4d0d-8042-1353aea65e97" alt="paddlepaddle" height="50px"/>](https://aistudio.baidu.com/overview) |

# 🗄️ 数据库
本项目使用`MySQL 5.7.44`作为数据库，数据库脚本文件并未存放在本项目中，您可以通过提交Issue的方式获取

# 🚀 运行
### 配置环境变量
在项目根目录创建并编辑`.env`文件，填写相应的变量值
```bash
SQLALCHEMY_DATABASE_URI = <your_mysql_uri>
REDIS_DATABASE_URI = <your_redis_uri>
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
# 🧩 系统架构
![image](https://github.com/user-attachments/assets/cdf5d549-6873-407c-bc39-3884f3a0a930)

# ✍ 写在最后
项目制作不易，如果它对你有帮助的话，请务必给作者点一个免费的⭐，万分感谢!🙏🙏🙏
