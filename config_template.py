import os

# Default User
USER_INFO = {
    "username": "admin",
    "password": "123456",
    "email": "admin@abc.com"
}

# Project ptah
PROJECT_FOLDER = f"{os.path.dirname(os.path.abspath(__file__))}/"
WORKFLOW_FOLDER = f'{PROJECT_FOLDER}workflow/'
TEMP_FOLDER = f'{PROJECT_FOLDER}temp/'
OUTPUT_FOLDER = f'{PROJECT_FOLDER}output/'
STATIC_FOLDER = f'{PROJECT_FOLDER}/app/static/'

# Database configuration
SQL_NAME = "comfyui-flask-webui"
SECRET_KEY = 'comfyui-flask-webui-2024'
SQLALCHEMY_DATABASE_URI = f'sqlite:///{PROJECT_FOLDER}/{SQL_NAME}.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Comfyui api ID
CLIENT_ID = "comfyui-flask-webui"

# Local web url
WEB_PORT = 8888
WEB_URL = f"http://127.0.0.1:{WEB_PORT}/"

# Local comfyui url
COMFYUI_PORT = 8188
COMFYUI_URL = f"http://127.0.0.1:{COMFYUI_PORT}/"
COMFYUI_WS_URL = f"ws://127.0.0.1:{COMFYUI_PORT}/"

# 百度翻译配置APPID和KEY
BD_FY_CONFIG = {
    "url": 'http://api.fanyi.baidu.com/api/trans/vip/translate',
    "appid": 'your_app_id',
    "secretKey": 'your_secret_key'
}
