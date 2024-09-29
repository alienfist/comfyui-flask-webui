from flask import Blueprint, render_template, request, jsonify

from .workflow import WP
from config import WORKFLOW_FOLDER
from .tools import save_original_image, save_generate_images
from utils.common import baidu_translate_tool
from utils.pic_tool import analyze_image_orientation


couple = Blueprint('couple', __name__)


@couple.route('/')
def index():
    return render_template('couple.html', active_page="couple")


@couple.route('/generate', methods=['POST'])
def gen_image_api():
    positive_prompt = request.form.get('positive_prompt', '')
    checkpoint = request.form.get('checkpoint')
    lora1 = request.form.get('lora1', '')
    lora2 = request.form.get('lora2', '')
    image_count = request.form.get('image_count')
    remove_bg = request.form.get('remove_bg')

    image_left_file = request.files.get('image_left_file')
    image_right_file = request.files.get('image_right_file')
    image_pose_file = request.files.get('image_pose_file')

    original_image_left_path = save_original_image(image_left_file)
    if not original_image_left_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    original_image_right_path = save_original_image(image_right_file)
    if not original_image_right_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    original_image_pose_path = save_original_image(image_pose_file)
    if not original_image_pose_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400
    res_orientation = analyze_image_orientation(original_image_pose_path)
    if res_orientation > 1.0:
        output_size = (1024, 768)
    else:
        output_size = (768, 1024)

    if positive_prompt:
        res_translate_positive_prompt = baidu_translate_tool(positive_prompt)
        positive_prompt = res_translate_positive_prompt["text"] if res_translate_positive_prompt["code"] == 1 else ""

    negative_prompt = ""
    gen_params = {
        "img_left_path": original_image_left_path,
        "img_right_path": original_image_right_path,
        "img_pose_path": original_image_pose_path,
        "model": checkpoint,
        "lora1": lora1,
        "lora2": lora2,
        "positive_prompt": positive_prompt,
        "negative_prompt": negative_prompt,
        "batch_size": image_count,
        "output_size": output_size
    }

    if remove_bg == "true":
        workflow_json = f"{WORKFLOW_FOLDER}workflow_couple_rmbg.json"
    else:
        workflow_json = f"{WORKFLOW_FOLDER}workflow_couple.json"

    gen_images = WP.process_couple(gen_params, workflow_json)
    if not gen_images:
        return jsonify({'status': 'error', 'message': 'gen couple failed.'}), 400

    image_type = 6
    images_url_list = save_generate_images(gen_images, gen_params, image_type)
    if not images_url_list:
        return jsonify({'status': 'error', 'message': 'save couple failed.'}), 400
    return jsonify({'status': 'success', "images_list": images_url_list})
