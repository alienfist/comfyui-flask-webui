from flask import Blueprint, render_template, request, jsonify

from .workflow import WP
from constants import BASE_PROMPT, DEFAULT_CHECKPOINT, LORA_PROMPT_MAPPING
from config import WORKFLOW_FOLDER
from .tools import save_generate_images
from utils.common import baidu_translate_tool


txt2img = Blueprint('txt2img', __name__)


@txt2img.route('/')
def index():
    return render_template('txt2img.html', active_page="txt2img")


@txt2img.route('/generate', methods=['POST'])
def gen_image_api():
    input_positive_prompt = request.form.get('positive_prompt', '')
    input_negative_prompt = request.form.get('negative_prompt', '')
    style = request.form.get('style', '')
    scale = request.form.get('scale', '')
    lora1 = request.form.get('lora1', '')
    lora1_weight = request.form.get('lora1_weight', '')
    lora2 = request.form.get('lora2', '')
    lora2_weight = request.form.get('lora2_weight', '')
    lora3 = request.form.get('lora3', '')
    lora3_weight = request.form.get('lora3_weight', '')
    checkpoint = request.form.get('checkpoint')
    image_count = request.form.get('image_count')
    remove_bg = request.form.get('remove_bg')

    if input_positive_prompt:
        res_translate_positive_prompt = baidu_translate_tool(input_positive_prompt)
        input_positive_prompt = res_translate_positive_prompt["text"] if res_translate_positive_prompt["code"] == 1 else ""
    positive_prompt = LORA_PROMPT_MAPPING.get(lora1, "") + LORA_PROMPT_MAPPING.get(lora2, "") + BASE_PROMPT["positive_prompt"] + input_positive_prompt

    if input_negative_prompt:
        translate_negative_prompt = baidu_translate_tool(input_negative_prompt)
        negative_prompt = translate_negative_prompt["text"] if translate_negative_prompt["code"] == 1 else ""
    else:
        negative_prompt = BASE_PROMPT["negative_prompt"]

    gen_params = {
        "positive_prompt": positive_prompt,
        "negative_prompt": negative_prompt,
        "batch_size": image_count,
        "scale": scale,
        "style": style,
        "lora1": lora1,
        "lora1_weight": lora1_weight,
        "lora2": lora2,
        "lora2_weight": lora2_weight,
        "lora3": lora3,
        "lora3_weight": lora3_weight,
        "checkpoint": checkpoint if checkpoint else DEFAULT_CHECKPOINT.get("txt2img"),
    }

    if remove_bg == "true":
        workflow_json = f"{WORKFLOW_FOLDER}workflow_txt2img_rmbg.json"
    else:
        workflow_json = f"{WORKFLOW_FOLDER}workflow_txt2img.json"
    gen_images = WP.process_txt2img(gen_params, workflow_json)
    if not gen_images:
        return jsonify({'status': 'error', 'message': 'gen txt2img failed.'}), 400

    image_type = 2
    images_url_list = save_generate_images(gen_images, gen_params, image_type)
    if not images_url_list:
        return jsonify({'status': 'error', 'message': 'save txt2img failed.'}), 400
    return jsonify({'status': 'success', "images_list": images_url_list})
