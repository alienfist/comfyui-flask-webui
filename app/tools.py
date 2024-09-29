import os
import time
import json
import shutil
from datetime import datetime

from utils.common import get_past_temp_folders
from utils.pic_tool import resize_image
from models import create_image, get_user_by_username
from constants import IMG_TYPE_MAPPING
from config import STATIC_FOLDER, USER_INFO


def save_original_image(image_file):
    """save original image and resize new image"""
    filename = int(time.time() * 1000000)
    temp_folder = f'{STATIC_FOLDER}{datetime.now().strftime("%Y%m%d")}/original/'
    os.makedirs(temp_folder, exist_ok=True)
    save_path = f'{temp_folder}{filename}.png'
    res_resize_image = resize_image(image_file, save_path, max_width=1000)
    if not res_resize_image:
        print("resize image failed.")
        return None
    return save_path


def save_generate_images(gen_images, gen_params, image_type):
    """gen image and insert url to sql"""
    images_url_list = []
    image_folder = f'{STATIC_FOLDER}{datetime.now().strftime("%Y%m%d")}/{IMG_TYPE_MAPPING[image_type]}/'
    os.makedirs(image_folder, exist_ok=True)
    user_uuid = get_user_by_username(USER_INFO["username"]).uuid
    for image_temp_path in gen_images:
        image_name = f"{int(time.time() * 1000000)}.png"
        image_save_path = f"{image_folder}{image_name}"
        shutil.copy2(image_temp_path, image_save_path)
        image_url = image_save_path.replace(STATIC_FOLDER, "static/")
        images_url_list.append(image_url)
        params = json.dumps(gen_params)
        create_image(image_url, params, image_type, user_uuid)
    return images_url_list


def clear_temp_folder():
    """delete temp folder"""
    try:
        past_temp_folders = get_past_temp_folders()
        for past_temp_folder in past_temp_folders:
            if os.path.isdir(past_temp_folder):
                shutil.rmtree(past_temp_folder)
        return True
    except Exception as e:
        print(e)
        return None
