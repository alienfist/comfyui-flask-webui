from flask import Blueprint, render_template, request, jsonify

from .workflow import WP
from .tools import save_original_image, save_generate_images
from utils.common import baidu_translate_tool

from config import WORKFLOW_FOLDER
from constants import DEFAULT_CHECKPOINT


art_photo = Blueprint('art_photo', __name__)


@art_photo.route('/')
def index():
    return render_template('art_photo.html', active_page="art_photo")


@art_photo.route('/generate', methods=['POST'])
def gen_art_photo_api():
    input_positive_prompt = request.form.get('positive_prompt', "")
    image_file = request.files.get('image_file')
    gender = request.form.get('gender')
    scale = request.form.get('scale')
    image_count = int(request.form.get('image_count'))
    original_image_path = save_original_image(image_file)
    if not original_image_path:
        return jsonify({'status': 'error', 'message': 'gen art photo failed.'}), 400

    if input_positive_prompt:
        res_translate_positive_prompt = baidu_translate_tool(input_positive_prompt)
        input_positive_prompt = res_translate_positive_prompt["text"] if res_translate_positive_prompt["code"] == 1 else ""
    positive_prompt = input_positive_prompt

    gen_params = {
        "checkpoint": DEFAULT_CHECKPOINT["art_photo"],
        "img_path": original_image_path,
        "scale": scale,
        "image_count": image_count,
        "positive_prompt": positive_prompt,
    }

    if gender == "female":
        workflow_json = f"{WORKFLOW_FOLDER}workflow_art_photo_female.json"
        gen_images = WP.process_art_photo(gen_params, workflow_json)
    else:
        workflow_json = f"{WORKFLOW_FOLDER}workflow_art_photo_male.json"
        gen_images = WP.process_art_photo_male(gen_params, workflow_json)

    if not gen_images:
        return jsonify({'status': 'error', 'message': 'gen art photo failed.'}), 400

    image_type = 8
    images_url_list = save_generate_images(gen_images, gen_params, image_type)
    if not images_url_list:
        return jsonify({'status': 'error', 'message': 'save art photo failed.'}), 400
    return jsonify({'status': 'success', "images_list": images_url_list})
