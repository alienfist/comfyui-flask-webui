from flask import Blueprint, render_template, request, jsonify

from .workflow import WP
from utils.common import baidu_translate_tool
from config import WORKFLOW_FOLDER
from .tools import save_original_image, save_generate_images


stickers = Blueprint("stickers", __name__)


@stickers.route('/')
def index():
    return render_template('stickers.html', active_page="stickers")


@stickers.route('/generate', methods=['POST'])
def gen_stickers_api():
    image_file = request.files.get('image_file')
    image_count = request.form.get('image_count')
    gender = request.form.get('gender')
    age = request.form.get('age')
    desc_prompt = request.form.get('descPrompt')
    style = request.form.get('style')
    remove_bg = request.form.get('remove_bg')

    original_image_path = save_original_image(image_file)
    if not original_image_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    style_dict = {
        "cartoon": "cutedoodle_XL-000012.safetensors",
        "cute": "SDXLFaeTastic2400.safetensors",
        "pure": "crystalz-sdxl-v2.safetensors",
        "gorgeous": "xl_yamer_style-3.0.safetensors",
        "realistic": "3D模型丨可爱化SDXL版_v2.0.safetensors",
    }

    if desc_prompt:
        desc_prompt_translate = baidu_translate_tool(desc_prompt)
        desc_prompt = desc_prompt_translate["text"] if desc_prompt_translate["code"] == 1 else desc_prompt
        positive_prompt = f"half body, looking at viewer, {age}, [{gender}], {desc_prompt}"
    else:
        positive_prompt = f"half body, looking at viewer, {age}, [{gender}]"
    gen_params = {
        "img_path": original_image_path,
        "positive_prompt": positive_prompt,
        "batch_size": int(image_count),
        "style_lora": style_dict[style],
        "sticker_lora": "",
    }

    if remove_bg == "true":
        workflow_json = f"{WORKFLOW_FOLDER}workflow_stickers_rmbg.json"
    else:
        workflow_json = f"{WORKFLOW_FOLDER}workflow_stickers.json"
    gen_images = WP.process_stickers(gen_params, workflow_json)
    if not gen_images:
        return jsonify({'status': 'error', 'message': 'gen sticker failed.'}), 400

    image_type = 1
    images_url_list = save_generate_images(gen_images, gen_params, image_type)
    if not images_url_list:
        return jsonify({'status': 'error', 'message': 'save stickers failed.'}), 400
    return jsonify({'status': 'success', "stickers_list": images_url_list})
