from flask import Blueprint, render_template, request, jsonify

from .workflow import WP
from constants import LORA_PROMPT_MAPPING
from config import WORKFLOW_FOLDER
from .tools import save_original_image, save_generate_images
from utils.common import baidu_translate_tool


img2img = Blueprint('img2img', __name__)


@img2img.route('/')
def index():
    return render_template('img2img.html', active_page="img2img")


@img2img.route('/generate', methods=['POST'])
def gen_image_api():
    input_positive_prompt = request.form.get('positive_prompt', "")
    image_file = request.files.get('image_file')
    style = request.form.get('style')
    divergence = request.form.get('divergence')
    original_image_path = save_original_image(image_file)
    if not original_image_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    style = style if style else "anime"
    style_dict = {
        "anime": {
            "model": "dreamshaperXL_v21TurboDPMSDE.safetensors",
            "lora": "StudioGhibli.Redmond-StdGBRRedmAF-StudioGhibli.safetensors",
            "negative_lora_prompt": "",
            "base_prompt": "anime artwork, anime style, key visual, vibrant, studio anime, highly detailed, ",
        },
        "chinese": {
            "model": "dreamshaperXL_v21TurboDPMSDE.safetensors",
            "lora": "国风插画SDXL.safetensors",
            "negative_lora_prompt": "",
            "base_prompt": "anime artwork, anime style, key visual, vibrant, studio anime, highly detailed, ",
        },
        "fantasy": {
            "model": "dreamshaperXL_v21TurboDPMSDE.safetensors",
            "lora": "SDXLFaeTastic2400.safetensors",
            "negative_lora_prompt": "",
            "base_prompt": "anime artwork, anime style, key visual, vibrant, studio anime, highly detailed, ",
        },
        "mud": {
            "model": "dreamshaperXL_v21TurboDPMSDE.safetensors",
            "lora": "CLAYMATE_V2.03_.safetensors",
            "negative_lora_prompt": "",
            "base_prompt": "anime artwork, anime style, key visual, vibrant, studio anime, highly detailed, ",
        },
        "princess": {
            "model": "realcartoonXL_v6.safetensors",
            "lora": "princess_xl_v2.safetensors",
            "negative_lora_prompt": "anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured, ",
            "base_prompt": "shallow depth of field, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy, ",
        },
        "pvc": {
            "model": "PVCStyleModelMovable_beta27Realistic.safetensors",
            "lora": "xl_more_art-full_v1.safetensors",
            "negative_lora_prompt": "",
            "base_prompt": "anime artwork, anime style, key visual, vibrant, studio anime, highly detailed, ",
        },
        "line": {
            "model": "dreamshaperXL_v21TurboDPMSDE.safetensors",
            "lora": "LineAniRedmondV2-Lineart-LineAniAF.safetensors",
            "negative_lora_prompt": "bad art, ugly, deformed, watermark, duplicated, ",
            "base_prompt": "best quality, anime, focus on face, manga, (lineart), (monochrome), black and white, (colorless),Lineart, LineAniAF, ",
        },
    }

    if input_positive_prompt:
        res_translate_positive_prompt = baidu_translate_tool(input_positive_prompt)
        input_positive_prompt = res_translate_positive_prompt["text"] if res_translate_positive_prompt["code"] == 1 else ""
    positive_prompt = style_dict[style]["base_prompt"] + input_positive_prompt

    negative_prompt = style_dict[style]["negative_lora_prompt"]
    gen_params = {
        "img_path": original_image_path,
        "model": style_dict[style]["model"],
        "divergence": divergence,
        "lora": style_dict[style]["lora"],
        "lora_prompt": LORA_PROMPT_MAPPING.get(style_dict[style]["lora"], ""),
        "positive_prompt": positive_prompt,
        "negative_prompt": negative_prompt,
    }

    workflow_json = f"{WORKFLOW_FOLDER}workflow_img2img.json"
    gen_images = WP.process_img2img(gen_params, workflow_json)
    if not gen_images:
        return jsonify({'status': 'error', 'message': 'gen img2img failed.'}), 400

    image_type = 3
    images_url_list = save_generate_images(gen_images, gen_params, image_type)
    if not images_url_list:
        return jsonify({'status': 'error', 'message': 'save img2img failed.'}), 400
    return jsonify({'status': 'success', "images_list": images_url_list})
