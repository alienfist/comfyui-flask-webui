import os
import time
import shutil
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify

from .workflow import WP
from utils.common import get_past_temp_folders
from utils.pic_tool import resize_image
from config import TEMP_FOLDER, WORKFLOW_FOLDER, STATIC_FOLDER


avatar = Blueprint("avatar", __name__)


@avatar.route('/')
def avatar_index():
    # 清理过去7天的临时文件
    past_temp_folders = get_past_temp_folders()
    for past_temp_folder in past_temp_folders:
        if os.path.isdir(past_temp_folder):
            shutil.rmtree(past_temp_folder)
    return render_template('avatar.html', active_page="avatar")


@avatar.route('/generate', methods=['POST'])
def gen_avatar_api():
    image_file = request.files.get('image_file')
    image_count = request.form.get('image_count')
    gender = request.form.get('gender')
    age = request.form.get('age')
    style = request.form.get('style')
    random_seed = request.form.get('random_seed')

    filename = int(time.time() * 1000000)
    suffix = image_file.filename.split(".")[-1]
    temp_folder = f'{TEMP_FOLDER}image/{datetime.now().strftime("%Y%m%d")}/'
    os.makedirs(temp_folder, exist_ok=True)
    temp_filepath = f'{temp_folder}{filename}.{suffix}'

    res_resize = resize_image(image_file, temp_filepath, max_width=1000)
    if not res_resize:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    style_dict = {
        "cartoon": "cutedoodle_XL-000012.safetensors",
        "cute": "SDXLFaeTastic2400.safetensors",
        "pure": "crystalz-sdxl-v2.safetensors",
        "gorgeous": "xl_yamer_style-3.0.safetensors",
        "realistic": "3D模型丨可爱化SDXL版_v2.0.safetensors",
    }

    gen_params = {
        "img_path": temp_filepath,
        "positive_prompt": f"half body, looking at viewer, {age}, [{gender}]",
        "batch_size": int(image_count),
        "style_lora": style_dict[style],
        "sticker_lora": "",
        "random_seed": True if random_seed == "true" else False
    }

    workflow_json = f"{WORKFLOW_FOLDER}workflow_stickers.json"
    res_gen_stickers = WP.process_stickers(gen_params, workflow_json)
    if not res_gen_stickers:
        return jsonify({'status': 'error', 'message': 'gen avatar failed.'}), 400

    stickers_list = [x.replace(f'{STATIC_FOLDER}', '/static/') for x in res_gen_stickers]
    return jsonify({'status': 'success', "stickers_list": stickers_list})
